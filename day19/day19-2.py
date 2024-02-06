#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "19"
partNumber = "2"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(),
  PanicThread.ONE_GIGABYTE,
  PanicThread.TEN_SECONDS)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # day{puzzleNumber}-{partNumber} # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

from enum import Enum

ACCEPTED = 'A'
REJECTED = 'R'

# sample part = {x=1, m=2, a=3, s=4}


class Operator(Enum):
    GT = '>'
    LT = '<'


class PartRanges:
    def __init__(self, nextWorkflow, ranges: {str: (int, int)}):
        self.nextWorkflow = nextWorkflow
        self.ranges = ranges

    def __str__(self):
        return f"{self.nextWorkflow}: {self.ranges}"


class Rule:
    def __init__(self, op: Operator, cat: str, value: int, destination: str):
        self.op = op
        self.cat = cat
        self.value = value
        self.destination = destination

    def isTrue(self, part):
        match self.op:
            case Operator.GT:
                return part[self.cat] > self.value
            case Operator.LT:
                return part[self.cat] < self.value
        return False

    def getSplit(self, partRanges) -> (PartRanges, PartRanges):
        debug(f"getSplits for {self} on {partRanges}")
        contRange = partRanges
        splitRange = None
        rangeForCat = contRange.ranges[self.cat]
        if self.value < rangeForCat[1] and self.value > rangeForCat[0]:
            splitRange = PartRanges(self.destination, partRanges.ranges.copy())
            if self.op == Operator.GT:
                contRange.ranges[self.cat] = (rangeForCat[0], self.value)
                splitRange.ranges[self.cat] = (self.value + 1, rangeForCat[1])
            elif self.op == Operator.LT:
                contRange.ranges[self.cat] = (self.value, rangeForCat[1])
                splitRange.ranges[self.cat] = (rangeForCat[0], self.value - 1)
        else:
            splitRange = None
        debug(f"\t return \n\t\t({contRange}, \n\t\t{splitRange})")
        return (contRange, splitRange)

    def __str__(self):
        return f"{self.cat}{'<' if self.op == Operator.LT else '>'}{self.value}:{self.destination}"


class Workflow:
    def __init__(self, label: str, rules: list[Rule], default: str):
        self.label = label
        self.rules = rules
        self.default = default

    def __str__(self):
        s = f"{self.label}" + "{"
        for i, rule in enumerate(self.rules):
            s += f"{rule},"
        s += f"{self.default}" + "}"
        return s


workflows = {}  # {label: Workflow}
iLines = 0
while lines[iLines] != "":
    line = lines[iLines]
    idxOpenB = line.find('{')
    idxCloseB = line.find('}')
    label = line[0:idxOpenB]
    partsSection = line[idxOpenB + 1:idxCloseB]
    parts = partsSection.split(',')
    rules = []
    for part in parts[0:-1]:
        debug(f"{part} {part.split(':')}")
        s = part.split(':')
        if '>' in s[0]:
            ss = s[0].split('>')
            debug(f"GT {Rule(Operator.GT, ss[0], int(ss[1]), s[1])}")
            rules.append(Rule(Operator.GT, ss[0], int(ss[1]), s[1]))
        elif '<' in s[0]:
            ss = s[0].split('<')
            debug(f"LT {Rule(Operator.LT, ss[0], int(ss[1]), s[1])}")
            rules.append(Rule(Operator.LT, ss[0], int(ss[1]), s[1]))
    workflows[label] = Workflow(label, rules, parts[-1])
    iLines += 1
debug(list(map(lambda wf: f"{wf}", workflows.values())))

partRanges = []
partRanges.append(PartRanges(
        'in',
        {
            'x': (1, 4000),
            'm': (1, 4000),
            'a': (1, 4000),
            's': (1, 4000)
        }))

acceptedPartRanges = []

while len(partRanges) > 0:
    partRange = partRanges[0]
    debug(f"{partRange}")
    if partRange.nextWorkflow == ACCEPTED:
        acceptedPartRanges.append(partRange)
        partRanges.remove(partRange)
        continue
    if partRange.nextWorkflow == REJECTED:
        partRanges.remove(partRange)
        continue

    wf = workflows[partRange.nextWorkflow]
    for rule in wf.rules:
        partRange, newRange = rule.getSplit(partRange)
        if newRange is not None:
            partRanges.append(newRange)

    debug(f"{partRanges[0].nextWorkflow} set to default {wf.default}")
    # debug(list(map(lambda x: f"{x}", partRanges)))
    partRanges[0].nextWorkflow = wf.default
    # debug(list(map(lambda x: f"{x}", partRanges)))

sumOfPossibleCombos = 0

for ranges in acceptedPartRanges:
    productOfDiffs = 1
    debug(f"{ranges}")
    for r in ranges.ranges.values():
        productOfDiffs *= r[1] - r[0]
    sumOfPossibleCombos += productOfDiffs

print(sumOfPossibleCombos)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
