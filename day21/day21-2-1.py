#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

import math

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "21"
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


# # # # #
debug(strGridRows())
# # # # #

STARTING_POSITION = 'S'
GARDEN_PLOT = '.'
ROCK = '#'


class GridRun:
    def __init__(
            self, 
            startingCoord: (int, int), 
            mapCountToExitCoords: {int, (int, int)}):
        self.startingCoord = startingCoord
        self.grid = []
        self._initGridWithBorder()
        self.nSteps = 0
        self.countHistory = []
        self.isRepeating = False
        self.evenRepeatCount = 0
        self.oddRepeatCount = 0
        self.mapCountToExitCoords = mapCountToExitCoords

    def __str__(self):
        sCountHistory = "["
        for count in self.countHistory:
            sCountHistory += str(count) + ","
        sCountHistory += "]"
        return f"{self.startingCoord}: {self.nSteps}, {self.isRepeating}, {self.evenRepeatCount}, {self.oddRepeatCount} \n{sCountHistory}\n{self._strGrid()}"

    # border of GARDEN_PLOT as input is formatted that way
    def _initGridWithBorder(self):
        self.grid.append([GARDEN_PLOT]*(nColumns + 2))
        # debug([GARDEN_PLOT]*(nColumns + 2))
        for row in gridRows:
            # debug(row)
            withBorder = [GARDEN_PLOT] + row + [GARDEN_PLOT]
            # debug(withBorder)
            self.grid.append(withBorder)
        self.grid.append([GARDEN_PLOT]*(nColumns + 2))
        # debug([GARDEN_PLOT]*(nColumns + 2))
        debug(self._strGrid())

    def _strGrid(self):
        s = "\n"
        for row in self.grid:
            for c in row:
                s += c
            s += "\n"
        return s

    def step(self):
        assert(not self.isRepeating, "no need to step a repeating grid")

        self.nSteps += 1
        nextCoords = []
        for i, row in enumerate(self.grid):
            hasNeighbour = False
            for j, c in enumerate(row):
                if c == ROCK:
                    continue

                # debug(f"determining neighbours for {i},{j}. {c}")

                # North
                if i > 0:
                    hasNeighbour = self._isNeighbour(i - 1, j)
                if hasNeighbour:
                    nextCoords.append((i, j))
                    hasNeighbour = False
                    continue
                # West
                if j > 0:
                    hasNeighbour = self._isNeighbour(i, j - 1)
                if hasNeighbour:
                    nextCoords.append((i, j))
                    hasNeighbour = False
                    continue
                # East
                if j < nColumnsMinusOne:
                    hasNeighbour = self._isNeighbour(i, j + 1)
                if hasNeighbour:
                    nextCoords.append((i, j))
                    hasNeighbour = False
                    continue
                # South
                if i < nRowsMinusOne:
                    hasNeighbour = self._isNeighbour(i + 1, j)
                if hasNeighbour:
                    nextCoords.append((i, j))
                    hasNeighbour = False
                    continue

        # clear positions
        for i, row in enumerate(self.grid):
            for j, c in enumerate(row):
                if c == REACHABLE_POSITION:
                    self.grid[i][j] = GARDEN_PLOT

        # fill positions
        for nextCoord in nextCoords:
            self.grid[nextCoord[0]][nextCoord[1]] = REACHABLE_POSITION

        # get reachable count
        self.countHistory.append(self._getReachableCount())

        # detect exits
        # for i, row in enumerate(self.grid):
            # if i == 0:
                # for j, c in enumerate(row):
                    # if c == REACHABLE_POSITION:
                        # self.mapCountToExitCoords[self.nSteps] = 
                            # (len(self.grid) - 1), j)
            # elif i == len(self.grid - 1):
                # for j, c in enumerate(row):
                    # if c == REACHABLE_POSITION:
                        # self.mapCountToExitCoords[self.nSteps] = 
                            # (0, j)
            # else:
                # if row[0] == REACHABLE_POSITION:
                   #  
            # for j, c in enumerate(row):
                # if c == REACHABLE_POSITION:
                    # self.grid[i][j] = GARDEN_PLOT

        # detect repeats
        if len(self.countHistory) > 3 and \
                self.countHistory[-1] == self.countHistory[-3]:
            self.isRepeating = True
            if self.nSteps%2 == 0:
                self.evenRepeatCount = self.countHistory[-1]
                self.oddRepeatCount = self.countHistory[-2]
            else:
                self.oddRepeatCount = self.countHistory[-1]
                self.evenRepeatCount = self.countHistory[-2]

        # # # # #
        # debug(strGridRows())
        # # # # #

    def _isNeighbour(self, i, j):
        return self.grid[i][j] == REACHABLE_POSITION

    def _getReachableCount(self):
        nReachable = 0
        for row in self.grid:
            for c in row:
                if c == REACHABLE_POSITION:
                    nReachable += 1
        return nReachable


# # # # #
debug(strGridRows())
# # # # #

mapGridRuns = {} # (startingCoord, GridRun)

startingI = math.ceil(nRows/2)
startingJ = math.ceil(nColumns/2)
startingCoord = (startingI, startingJ)
mapGridRuns[startingCoord] = GridRun(startingCoord,{})

debug(mapGridRuns.keys())

while (len(mapGridRuns) > 0):
    for mgr in mapGridRuns.values():
        while True:
            mgr.step()
            debug(str(mgr))
            if mgr.isRepeating:
                mapGridRuns.pop(mgr.startingCoord)
                break

print(nReachable)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
