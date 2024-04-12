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
  # PanicThread.TEN_SECONDS)
  PanicThread.TWO_MINUTES)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-simple.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-2.txt", 'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # day{puzzleNumber}-{partNumber} # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

nRowsMinusOne = nRows - 1
nColumnsMinusOne = nColumns - 1

STARTING_POSITION = 'S'
REACHABLE_POSITION = 'O'
GARDEN_PLOT = '.'

gridRows = []

for line in lines:
    # line = line.replace(STARTING_POSITION, REACHABLE_POSITION)
    line = line.replace(STARTING_POSITION, GARDEN_PLOT)
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
ROCK = '#'


class GridRun:
    def __init__(self):
        self.grid = []
        self._initGridWithBorder()
        self.gridHeightMinusOne = len(self.grid) - 1
        self.gridWidthMinusOne = len(self.grid[0]) - 1
        self.nSteps = 0
        self.countHistory = []
        self.isRepeating = False
        self.evenRepeatCount = 0
        self.oddRepeatCount = 0

    def __str__(self):
        sCountHistory = "["
        for count in self.countHistory:
            sCountHistory += str(count) + ","
        sCountHistory += "]"
        return f"{self.nSteps}, {self.isRepeating}, {self.evenRepeatCount}, {self.oddRepeatCount} \n{sCountHistory}\n{self._strGrid()}"
        # return f"{self.nSteps}, {self.isRepeating}, {self.evenRepeatCount}, {self.oddRepeatCount} \n{sCountHistory}"

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

        sp = self.getStartPosition()
        debug(sp)
        self.grid[sp[0]][sp[1]] = REACHABLE_POSITION

        # debug([GARDEN_PLOT]*(nColumns + 2))
        # debug(f"\n{self._strGrid()}")

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
                if j < self.gridWidthMinusOne:
                    hasNeighbour = self._isNeighbour(i, j + 1)
                if hasNeighbour:
                    nextCoords.append((i, j))
                    hasNeighbour = False
                    continue
                # South
                if i < self.gridHeightMinusOne:
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

        # detect repeats
        if len(self.countHistory) > 3 and \
                self.countHistory[-1] == self.countHistory[-3]:
            self.isRepeating = True
            if self.nSteps % 2 == 0:
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
        for i, row in enumerate(self.grid):
            # if not border row
            if i > 0 and i < len(self.grid) - 1:
                for j, c in enumerate(row):
                    if j > 0 and j < len(row) - 1 and \
                            c == REACHABLE_POSITION:
                        nReachable += 1
        return nReachable

    def getStartPosition(self):
        raise NotImplementedError()

    def generateExitGridRuns(self, nSteps):
        raise NotImplementedError()


KEY_CENTER = "C"
KEY_NORTH = "N"
KEY_SOUTH = "S"
KEY_EAST = "E"
KEY_WEST = "W"
KEY_SE = "SE"
KEY_SW = "SW"
KEY_NE = "NE"
KEY_NW = "NW"


class NorthGridRun(GridRun):
    def getStartPosition(self):
        return (0, math.ceil(nColumns/2))

    def generateExitGridRuns(self, nSteps):
        if nSteps == nRows:
            return {KEY_NORTH: NorthGridRun()}
        else:
            return []


class SouthGridRun(GridRun):
    def getStartPosition(self):
        return (nRows - 1 + 2, math.ceil(nColumns/2))  # plus 2 for border

    def generateExitGridRuns(self, nSteps):
        if nSteps == nRows:
            return {KEY_SOUTH: SouthGridRun()}
        else:
            return []


class WestGridRun(GridRun):
    def getStartPosition(self):
        return (math.ceil(nRows/2), 0)

    def generateExitGridRuns(self, nSteps):
        if nSteps == nColumns:
            return {KEY_WEST: WestGridRun()}
        else:
            return []


class EastGridRun(GridRun):
    def getStartPosition(self):
        return (math.ceil(nRows/2), nColumns - 1 + 2)  # plus 2 for border

    def generateExitGridRuns(self, nSteps):
        if nSteps == nColumns:
            return {KEY_EAST: EastGridRun()}
        else:
            return []


class DiagonalGridRun(GridRun):

    def getKey():
        raise NotImplementedError()

    def getNewInstance():
        raise NotImplementedError()

    def generateExitGridRuns(self, nSteps):
        if nSteps == nRows * 2:  # assuming grid is square
            return {self.getKey(): self.getNewInstance()}
        else:
            return []


class NEGridRun(DiagonalGridRun):
    def getKey():
        return KEY_NE

    def getStartPosition(self):
        return (0, 0)


class NWGridRun(DiagonalGridRun):
    def getKey():
        return KEY_NW

    def getStartPosition(self):
        return (0, nColumns - 1 + 2)  # plus two for border


class SEGridRun(DiagonalGridRun):
    def getKey():
        return KEY_SE

    def getStartPosition(self):
        return (nRows - 1 + 2, 0)  # plus two for border


class SWGridRun(DiagonalGridRun):
    def getKey():
        return KEY_SW

    def getStartPosition(self):
        return (nRows - 1 + 2, nColumns - 1 + 2)  # plus two for border


class CenterGridRun(GridRun):
    def getKey(self):
        return KEY_CENTER

    def getStartPosition(self):
        return (math.ceil(nRows/2), math.ceil(nColumns/2))

    def generateExitGridRuns(self, nSteps):
        if nSteps == math.ceil(nRows/2):  # assuming square grid
            debug("center cardinal exits")
            return {KEY_NORTH: NorthGridRun(),
                    KEY_SOUTH: SouthGridRun(),
                    KEY_WEST: WestGridRun(),
                    KEY_EAST: EastGridRun()}
        elif nSteps == nRows:  # assuming square grid
            debug("diagonal cardinal exits")
            return {KEY_NE: NEGridRun(),
                    KEY_SE: SEGridRun(),
                    KEY_NW: NWGridRun(),
                    KEY_SW: SWGridRun()}
        else:
            return []


# # # # #
debug(strGridRows())
# # # # #

nSteps = 0
mapGridRuns = {KEY_CENTER: CenterGridRun()}  # (startingCoord, GridRun)

repeatingGridRuns = {}

debug(mapGridRuns.keys())

while (len(mapGridRuns) > 0):
    repeatingGridRunKeys = []
    newGridRuns = {}
    for key, mgr in mapGridRuns.items():
        while True:
            if mgr.isRepeating:
                break
            nSteps += 1
            mgr.step()
            newRuns = mgr.generateExitGridRuns(nSteps)
            if len(newRuns) > 0:
                for k, newRun in newRuns.items():
                    if not (k in repeatingGridRunKeys or
                            k in mapGridRuns):
                        newGridRuns[k] = newRun
            # debug(mgr.nSteps)
            if mgr.nSteps in [nRows, math.floor(nRows/2), nRows + math.floor(nRows/2)]:
                debug(str(mgr))
        if mgr.isRepeating:
            repeatingGridRunKeys.append(key)
            continue
    for key in repeatingGridRunKeys:
        debug(f"repeating grid run key: {key}")
        repeatingGridRuns[key] = mapGridRuns[key]
        mapGridRuns.pop(key)
    if len(newGridRuns) > 0:
        mapGridRuns = {**newGridRuns, **mapGridRuns}

for key, mgr in repeatingGridRuns.items():
    debug(f"{key}, {mgr}")

stepLimit = 26501365
# stepLimit = 131 + 131 + 131 + 65
stepLimitMinusFirstCenterExitSteps = stepLimit - math.floor(nRows/2)
nGridsNorthAfterCenter = \
        math.floor(stepLimitMinusFirstCenterExitSteps/nRows)
nRemainderNorth = stepLimitMinusFirstCenterExitSteps % nRows
# isRemainderPastHalf = nRemainderNorth >= math.floor(nRows/2)

debug(f"{stepLimit}, {stepLimitMinusFirstCenterExitSteps}, {nGridsNorthAfterCenter}, {nRemainderNorth}")

nFullGridsNorth = nGridsNorthAfterCenter - 1
# if remainder is not past half, second to last full sqaure is not full
# if not isRemainderPastHalf:
    # nFullGridsNorth -= 1

# hogben's central polygonal numbers
nFullGrids = 2 * (nFullGridsNorth*nFullGridsNorth) + 2 * nFullGridsNorth + 1


debug(f"nRemainderNorth:{nRemainderNorth}, nFullGridsNorth:{nFullGridsNorth}, nFullGrids: {nFullGrids}")

nStepsPastFullGrids = nRemainderNorth
# if not isRemainderPastHalf:
    # nStepsPastFullGrids += nRows

# determine count for full grid, key is arbitrary assuming all grids reach same numbers
isEven = stepLimit % 2 == 0
nCountForFullGrid = 0
if isEven:
    nCountForFullGrid = repeatingGridRuns[KEY_NORTH].evenRepeatCount
else:
    nCountForFullGrid = repeatingGridRuns[KEY_NORTH].oddRepeatCount

debug(f"{nStepsPastFullGrids}, {nCountForFullGrid}")

totalCount = 0

# full grids
totalCount += nCountForFullGrid * nFullGrids

debug(totalCount)

# 4 leading corners
for key in [KEY_NORTH, KEY_WEST, KEY_SOUTH, KEY_EAST]:
    # debug(f"{key} {repeatingGridRuns[key].countHistory[nRows]}")
    totalCount += repeatingGridRuns[key].countHistory[nRows - 1]
    # if not isRemainderPastHalf:
        # totalCount += repeatingGridRuns[key].countHistory[nStepsPastFullGrids]

debug(totalCount)

# non-full sides, outter
for i in range(nFullGridsNorth):
    for key in [KEY_NE, KEY_NW, KEY_SE, KEY_SW]:
        # debug(f"{key} {repeatingGridRuns[key].countHistory[math.floor(nRows/2)]}")
        totalCount += repeatingGridRuns[key].countHistory[math.floor(nRows/2) - 1]

debug(totalCount)

# non-full sides, inner
for i in range(nFullGridsNorth - 1):
    for key in [KEY_NE, KEY_NW, KEY_SE, KEY_SW]:
        # debug(f"{key} {repeatingGridRuns[key].countHistory[nRows + math.floor(nRows/2)]}")
        totalCount += repeatingGridRuns[key].countHistory[nRows + math.floor(nRows/2) - 1]


debug(f"N partial: {repeatingGridRuns[KEY_NORTH].countHistory[nRows - 1]}")
debug(f"W partial: {repeatingGridRuns[KEY_WEST].countHistory[nRows - 1]}")
debug(f"E partial: {repeatingGridRuns[KEY_EAST].countHistory[nRows - 1]}")
debug(f"S partial: {repeatingGridRuns[KEY_SOUTH].countHistory[nRows - 1]}")
debug(f"NW 1/4: {repeatingGridRuns[KEY_NW].countHistory[math.floor(nRows/2) - 1]}")
debug(f"NE 1/4: {repeatingGridRuns[KEY_NE].countHistory[math.floor(nRows/2) - 1]}")
debug(f"SW 1/4: {repeatingGridRuns[KEY_SW].countHistory[math.floor(nRows/2) - 1]}")
debug(f"SE 1/4: {repeatingGridRuns[KEY_SE].countHistory[math.floor(nRows/2) - 1]}")
debug(f"NW 3/4: {repeatingGridRuns[KEY_NW].countHistory[nRows + math.floor(nRows/2) - 1]}")
debug(f"NE 3/4: {repeatingGridRuns[KEY_NE].countHistory[nRows + math.floor(nRows/2) - 1]}")
debug(f"SW 3/4: {repeatingGridRuns[KEY_SW].countHistory[nRows + math.floor(nRows/2) - 1]}")
debug(f"SE 3/4: {repeatingGridRuns[KEY_SE].countHistory[nRows + math.floor(nRows/2) - 1]}")


print(totalCount)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
