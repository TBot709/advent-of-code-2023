#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "21"
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
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-simple.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt", 'r')
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

nRowsMinusOne = nRows - 1
nColumnsMinusOne = nColumns - 1

STARTING_POSITION = 'S'
REACHABLE_POSITION = 'O'

gridRows = []

for line in lines:
    line = line.replace(STARTING_POSITION, REACHABLE_POSITION)
    row = []
    for c in line:
        row.append(c)
    gridRows.append(row)


def strGridRows():
    s = "\n"
    for row in gridRows:
        for c in row:
            s += c
        s += "\n"
    return s


def getReachableCount():
    count = 0
    for row in gridRows:
        for c in row:
            if c == REACHABLE_POSITION:
                count += 1
    return count


# # # # #
debug(strGridRows())
# # # # #

STARTING_POSITION = 'S'
GARDEN_PLOT = '.'
ROCK = '#'


def isNeighbour(i, j):
    # debug(f"\tis neighbour at {i},{j}? {gridRows[i][j]}")
    return gridRows[i][j] == REACHABLE_POSITION


numSteps = 128 + 64 # 64
while numSteps > 0:
    # check what positions will be reachable at end of this step
    positionsToUpdate = []
    for i, row in enumerate(gridRows):
        hasNeighbour = False
        for j, c in enumerate(row):
            if c == ROCK:
                continue

            # debug(f"determining neighbours for {i},{j}. {c}")

            # North
            if i > 0:
                hasNeighbour = isNeighbour(i - 1, j)
            if hasNeighbour:
                positionsToUpdate.append((i, j))
                hasNeighbour = False
                continue
            # West
            if j > 0:
                hasNeighbour = isNeighbour(i, j - 1)
            if hasNeighbour:
                positionsToUpdate.append((i, j))
                hasNeighbour = False
                continue
            # East
            if j < nColumnsMinusOne:
                hasNeighbour = isNeighbour(i, j + 1)
            if hasNeighbour:
                positionsToUpdate.append((i, j))
                hasNeighbour = False
                continue
            # South
            if i < nRowsMinusOne:
                hasNeighbour = isNeighbour(i + 1, j)
            if hasNeighbour:
                positionsToUpdate.append((i, j))
                hasNeighbour = False
                continue

    # clear positions
    for i, row in enumerate(gridRows):
        for j, c in enumerate(row):
            if c == REACHABLE_POSITION:
                gridRows[i][j] = GARDEN_PLOT

    # fill positions
    for positionToUpdate in positionsToUpdate:
        gridRows[positionToUpdate[0]][positionToUpdate[1]] = REACHABLE_POSITION

    # # # # #
    # debug(strGridRows())
    # # # # #

    debug(getReachableCount())

    numSteps -= 1

# # # # #
debug(strGridRows())
# # # # #

print(getReachableCount())

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
