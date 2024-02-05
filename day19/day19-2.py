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
        self.ranges

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
        contRange = partRanges
        splitRange = partRanges
        match self.op:
            case Operator.GT:
                contRange.ranges[self.cat][1] == self.value
                splitRange.ranges[self.cat][0] == self.value + 1
            case Operator.LT:
                contRange.ranges[self.cat][0] == self.value + 1
                splitRange.ranges[self.cat][1] == self.value
        return (contRange, splitRange)
                

    def __str__(self):
        return f"{self.cat}{'<' if self.cat == Operator.LT else '>'}{self.value}:{self.destination}"


class Workflow:
    def __init__(self, label: str, rules: list[Rule], default: str):
        self.label = label
        self.rules = rules
        self.default = default

    def getSplits(self, partRanges):
        splits = partRange

    def __str__(self):
        s = f"{self.label}" + "{"
        for i, rule in enumerate(self.rules):
            s += f"{rule.cat}{'<' if rule.cat == Operator.LT else '>'}{rule.value}:{rule.destination},"
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
        s = part.split(':')
        if '>' in s[0]:
            ss = s[0].split('>')
            rules.append(Rule(Operator.GT, ss[0], int(ss[1]), s[1]))
        elif '<' in s[0]:
            ss = s[0].split('<')
            rules.append(Rule(Operator.LT, ss[0], int(ss[1]), s[1]))
    workflows[label] = Workflow(label, rules, parts[-1])
    iLines += 1
debug(list(map(lambda wf: f"{wf}", workflows.values())))

partRanges[0] = 
    PartRange('in', 
            {'x': (1, 4000), 
                'm': (1, 4000), 
                'a': (1, 4000), 
                's': (1, 4000)})

acceptedPartRanges = []

for partRange in partRanges:
    nxt = workflows[].getNext(part)
    while nxt not in [ACCEPTED, REJECTED]:
        nxt = workflows[nxt].getNext(part)
    if nxt == ACCEPTED:
        ratingSum += sum(part.values())

print(ratingSum)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
