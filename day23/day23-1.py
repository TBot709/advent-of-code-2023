#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "23"
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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}-smaller-input.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}-small-input.txt", 'r')
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

grid = []
for line in lines:
    row = []
    for c in line:
        row.append(c)
    grid.append(row)


def strGrid():
    s = "\n"
    for row in grid:
        for c in row:
            s += c
        s += "\n"
    return s


debug(strGrid())

WALL = '#'
PATH = '.'
SLOPE_N = '^'
SLOPE_W = '<'
SLOPE_E = '>'
SLOPE_S = 'v'
NORTH = 'N'
WEST = 'W'
EAST = 'E'
SOUTH = 'S'

directions = [NORTH, WEST, EAST, SOUTH]
dirTransitions = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # N W E S
slopes = [SLOPE_N, SLOPE_W, SLOPE_E, SLOPE_S]


def getTranslation(coord: (int, int), direction: str):
    dtIndex = 0
    if direction == NORTH:
        dtIndex = 0
    elif direction == WEST:
        dtIndex = 1
    elif direction == EAST:
        dtIndex = 2
    elif direction == SOUTH:
        dtIndex = 3
    return (coord[0] + dirTransitions[dtIndex][0],
            coord[1] + dirTransitions[dtIndex][1])


def getSlopeTranslation(coord: (int, int), slope: str):
    if slope == SLOPE_N:
        return getTranslation(coord, NORTH)
    elif slope == SLOPE_W:
        return getTranslation(coord, WEST)
    elif slope == SLOPE_E:
        return getTranslation(coord, EAST)
    elif slope == SLOPE_S:
        return getTranslation(coord, SOUTH)


def isCharAtCoord(char: str, coord: (int, int)):
    if (coord[0] < 0 or coord[0] >= nColumns or
            coord[1] < 0 or coord[1] >= nRows):
        return False
    return grid[coord[1]][coord[0]] == char


def isSlopeAtCoord(coord: (int, int)):
    if (coord[0] < 0 or coord[0] >= nColumns or
            coord[1] < 0 or coord[1] >= nRows):
        return False
    return grid[coord[1]][coord[0]] in slopes


def getCharAtCoord(coord: (int, int)):
    return grid[coord[1]][coord[0]]


class Node:
    def __init__(self, coord):
        self.coord = coord

        self.entrySlopeCoords = {}
        t = getTranslation(self.coord, NORTH)
        if isCharAtCoord(SLOPE_S, t):
            self.entrySlopeCoords[NORTH] = t
        t = getTranslation(self.coord, WEST)
        if isCharAtCoord(SLOPE_E, t):
            self.entrySlopeCoords[WEST] = t
        t = getTranslation(self.coord, EAST)
        if isCharAtCoord(SLOPE_W, t):
            self.entrySlopeCoords[EAST] = t
        t = getTranslation(self.coord, SOUTH)
        if isCharAtCoord(SLOPE_N, t):
            self.entrySlopeCoords[SOUTH] = t

        self.exitSlopeCoords = {}
        t = getTranslation(self.coord, NORTH)
        if isCharAtCoord(SLOPE_N, t):
            self.exitSlopeCoords[NORTH] = t
        t = getTranslation(self.coord, WEST)
        if isCharAtCoord(SLOPE_W, t):
            self.exitSlopeCoords[WEST] = t
        t = getTranslation(self.coord, EAST)
        if isCharAtCoord(SLOPE_E, t):
            self.exitSlopeCoords[EAST] = t
        t = getTranslation(self.coord, SOUTH)
        if isCharAtCoord(SLOPE_S, t):
            self.exitSlopeCoords[SOUTH] = t

    def __str__(self):
        return f"{self.coord}, {self.entrySlopeCoords}, {self.exitSlopeCoords}"

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]


endNodeCoord = (nColumns - 2, nRows - 1)
debug(f"endNodeCoord: {endNodeCoord}")
# endNode = Node(endNodeCoord)
startNode = Node((1, 0))
startNode.exitSlopeCoords[SOUTH] = (1, 0)

nodes = [startNode]

adjacencies = {}
adjacencies[startNode.coord] = {}  # no paths to start

for departNode in nodes:
    debug(f"{departNode}")
    for slopeD in directions:
        debug(f"\t{slopeD}")
        c = ()
        slope = ()
        if slopeD in departNode.exitSlopeCoords:
            slope = departNode.exitSlopeCoords[slopeD]
            c = getTranslation(slope, slopeD)
        else:
            continue

        stepCount = 1
        prevC = slope
        isSlopeReached = False
        while not isSlopeReached:
            nextDir = ""
            for nxtD in directions:
                nxt = getTranslation(c, nxtD)
                # debug(f"\t\tcurrent:{c} {nxtD} next:{nxt} prev:{prevC} steps:{stepCount}")
                if prevC is not None and nxt == prevC:
                    continue

                if nxt == endNodeCoord:
                    stepCount += 1
                    nodes.append(Node(endNodeCoord))
                    adjacencies[endNodeCoord] = {departNode.coord: stepCount}
                    debug(str(nodes[-1]))
                    isSlopeReached = True  # not a slope, but we want exit

                if isCharAtCoord(PATH, nxt):
                    prevC = tuple(c)
                    c = tuple(nxt)
                    stepCount += 1
                elif isSlopeAtCoord(nxt):
                    prevC = tuple(nxt)
                    c = getSlopeTranslation(nxt, getCharAtCoord(nxt))
                    stepCount += 2

                    if c not in adjacencies:
                        nodes.append(Node(tuple(c)))
                        adjacencies[tuple(c)] = {}

                    # only keep longer path if multipl exist
                    if departNode.coord not in adjacencies[tuple(c)]:
                        adjacencies[tuple(c)][departNode.coord] = 0

                    if adjacencies[tuple(c)][departNode.coord] < stepCount:
                        adjacencies[tuple(c)][departNode.coord] = stepCount

                    debug(str(nodes[-1]))
                    isSlopeReached = True
                    break

debug(f"num nodes = {len(nodes)}")

for node in nodes:
    grid[node.coord[1]][node.coord[0]] = 'N'

debug(strGrid())

debug(adjacencies)

paths = []


def findPath(pathSoFar: [((int, int), int)]):
    currentNodeCoord = pathSoFar[-1][0]
    if currentNodeCoord == startNode.coord:
        paths.append(pathSoFar)
    for coord, distance in adjacencies[currentNodeCoord].items():
        p = list(pathSoFar)
        p.append((coord, distance))
        findPath(p)


findPath([(endNodeCoord, 0)])

debug(str(paths).replace('],','],\n'))

pathLengths = \
    list(map(lambda p: sum(map(lambda n: n[1], p)) + len(p) - 2, paths))

debug(pathLengths)

maxPath = max(pathLengths)

print(maxPath)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
