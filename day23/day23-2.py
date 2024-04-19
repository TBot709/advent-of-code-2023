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
partNumber = "2"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(),
  PanicThread.ONE_GIGABYTE,
  # PanicThread.TEN_SECONDS)
  PanicThread.ONE_HOUR)
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

# remove slopes
grid = \
        list(map(lambda row:
                 list(map(lambda c:
                          c.replace(SLOPE_N, PATH)
                          .replace(SLOPE_W, PATH)
                          .replace(SLOPE_E, PATH)
                          .replace(SLOPE_S, PATH),
                          row)),
                 grid))

debug(strGrid())

directions = [NORTH, WEST, EAST, SOUTH]
dirTransitions = [(0, -1), (-1, 0), (1, 0), (0, 1)]  # N W E S


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


def isCharAtCoord(char: str, coord: (int, int)):
    if (coord[0] < 0 or coord[0] >= nColumns or
            coord[1] < 0 or coord[1] >= nRows):
        return False
    return grid[coord[1]][coord[0]] == char


def getCharAtCoord(coord: (int, int)):
    return grid[coord[1]][coord[0]]


def getAdjacentPathCount(coord: (int, int)):
    pathCount = 0
    t = getTranslation(coord, NORTH)
    if isCharAtCoord(PATH, t):
        pathCount += 1
    t = getTranslation(coord, WEST)
    if isCharAtCoord(PATH, t):
        pathCount += 1
    t = getTranslation(coord, EAST)
    if isCharAtCoord(PATH, t):
        pathCount += 1
    t = getTranslation(coord, SOUTH)
    if isCharAtCoord(PATH, t):
        pathCount += 1
    return pathCount


class Node:
    def __init__(self, coord):
        self.coord = coord

        self.exitCoords = {}
        t = getTranslation(self.coord, NORTH)
        if isCharAtCoord(PATH, t):
            self.exitCoords[NORTH] = t
        t = getTranslation(self.coord, WEST)
        if isCharAtCoord(PATH, t):
            self.exitCoords[WEST] = t
        t = getTranslation(self.coord, EAST)
        if isCharAtCoord(PATH, t):
            self.exitCoords[EAST] = t
        t = getTranslation(self.coord, SOUTH)
        if isCharAtCoord(PATH, t):
            self.exitCoords[SOUTH] = t

    def __str__(self):
        return f"{self.coord}, {self.exitCoords}"

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.coord[0] == other.coord[0] and self.coord[1] == other.coord[1]


endNodeCoord = (nColumns - 2, nRows - 1)
debug(f"endNodeCoord: {endNodeCoord}")
# endNode = Node(endNodeCoord)
startNode = Node((1, 0))
startNode.exitCoords[SOUTH] = (1, 1)

nodes = [startNode]

adjacencies = {}
adjacencies[startNode.coord] = {}  # no paths to start

for i, departNode in enumerate(nodes):
    debug(f"{i} {departNode}")
    for exitCoord in departNode.exitCoords.values():
        debug(f"\t{exitCoord}")

        if exitCoord == departNode.coord:
            continue

        c = exitCoord
        prevC = departNode.coord
        stepCount = 1
        isNextNodeReached = False
        while not isNextNodeReached:
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
                    isNextNodeReached = True
                    break

                if isCharAtCoord(PATH, nxt):
                    prevC = tuple(c)
                    c = tuple(nxt)
                    stepCount += 1
                    if c in adjacencies.keys() or \
                            getAdjacentPathCount(c) > 2:
                        isNextNodeReached = True

                        if c not in adjacencies:
                            nodes.append(Node(tuple(c)))
                            adjacencies[tuple(c)] = {}

                        if departNode.coord not in adjacencies[tuple(c)]:
                            adjacencies[c][departNode.coord] = 0

                        # only keep longer path if multiple
                        if adjacencies[c][departNode.coord] < stepCount:
                            adjacencies[c][departNode.coord] = stepCount

                        break

debug(f"num nodes = {len(nodes)}")

for node in nodes:
    grid[node.coord[1]][node.coord[0]] = 'N'

# debug(strGrid())

debug("adjacencies: \n" + str(adjacencies).replace('},', '},\n'))

paths = []


def findPath(pathSoFar: [((int, int), int)]):
    currentNodeCoord = pathSoFar[-1][0]
    if currentNodeCoord == startNode.coord:
        # debug("new path: " + str(pathSoFar))
        paths.append(pathSoFar)
    for coord, distance in adjacencies[currentNodeCoord].items():
        p = list(pathSoFar)
        p.append((coord, distance))
        if len(set(list(map(lambda cAndD: cAndD[0], p)))) == len(p):
            findPath(p)


findPath([(endNodeCoord, 0)])

# debug("paths: \n" + str(paths).replace('],', '],\n'))

pathLengths = \
    list(map(lambda p: sum(map(lambda n: n[1], p)), paths))

debug(pathLengths)

maxPath = max(pathLengths)

print(maxPath)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
