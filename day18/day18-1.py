#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "18"
partNumber = "1"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(),
  PanicThread.ONE_GIGABYTE,
  PanicThread.TEN_SECONDS)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt", 'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
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

DUG = '#'
FLAT = '.'

class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


class DigPlanEntry:
    def __init__(self, direction: Direction, distance: int, color: str):
        self.direction = direction
        self.distance = distance
        self.color = color

    def __str__(self):
        return f"{self.direction.value} {self.distance} {self.color}"


digPlan = []
for line in lines:
    l_s = line.split()
    digPlan.append(DigPlanEntry(Direction(l_s[0]), int(l_s[1]), l_s[2]))


def sDigPlan(digPlan):
    s = '\n'
    for entry in digPlan:
        s += str(entry) + '\n'
    return s


debug(sDigPlan(digPlan))


class GridCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class TrenchEdge(GridCell):
    def __init__(self, x, y, color):
        GridCell.__init__(self, x, y)
        self.color = color


def sGrid(grid):
    minX = min(cell.x for cell in grid.values())
    maxX = max(cell.x for cell in grid.values())
    minY = min(cell.y for cell in grid.values())
    maxY = max(cell.y for cell in grid.values())

    s = '\n'
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if (x, y) in grid:
                s += DUG
            else:
                s += FLAT
        s += '\n'
    return s


cX = 0
cY = 0
grid = {}
# grid[(cX, cY)] = TrenchEdge(cX, cY, digPlan[0].color)
for entry in digPlan:
    # debug(entry)
    for i in range(0, entry.distance):
        if entry.direction == Direction.UP:
            cY -= 1
        if entry.direction == Direction.DOWN:
            cY += 1
        if entry.direction == Direction.LEFT:
            cX -= 1
        if entry.direction == Direction.RIGHT:
            cX += 1
        grid[(cX, cY)] = TrenchEdge(cX, cY, entry.color)
    # debug(sGrid(grid))


gridString = sGrid(grid)

debug(gridString)

from day18.scanfill import scanfill

gridStringDugOut = scanfill(gridString, '#', '.')

'''
isInside = False
previousCell = FLAT
for iC, c in enumerate(gridString):
    if c == FLAT and previousCell == DUG:
        isInside = not isInside

    previousCell = c
    charToAdd = c
    if c == '\n':
        previousCell = FLAT
        isInside = False
    elif isInside:
        charToAdd = DUG

    debug(f"{iC}, {c}, {isInside} {previousCell}")

    gridStringDugOut += charToAdd
'''


debug('\n' + gridStringDugOut)

dugCount = 0
for c in gridStringDugOut:
    if c == DUG:
        dugCount += 1

print(dugCount)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
