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

from day18.day18_common import Direction, Edge, Corner
from coord import Coord
from day18.scancount import scancount

DUG = '#'
FLAT = '.'


def getDistanceAndDirection(colorString):
    # colorString, Hex, Direction (#HHHHHD)
    distanceInHex = colorString[2:7:]
    distance = int(distanceInHex, 16)

    directionNumber = colorString[7]
    direction = Direction.UNKNOWN
    match directionNumber:
        case "0": direction = Direction.RIGHT
        case "1": direction = Direction.DOWN
        case "2": direction = Direction.LEFT
        case "3": direction = Direction.UP
    if direction == Direction.UNKNOWN:
        raise Exception("unhandled directionCode, " + directionNumber)

    debug(f"{colorString}, {distance}, {direction}")
    return (distance, direction)


class DigPlanEntry:
    def __init__(self, color: str):
        distanceAndDirection = getDistanceAndDirection(color)
        self.direction = distanceAndDirection[1]
        self.distance = distanceAndDirection[0]
        self.color = color

    '''
    # same as day18-1 init, used while debuging shoelace algo
    def __init__(self, direction, distance, color):
        self.direction = direction
        self.distance = distance
        self.color = color
    '''

    def __str__(self):
        return f"{self.direction.value} {self.distance} {self.color}"


digPlan = []
for line in lines:
    l_s = line.split()
    digPlan.append(DigPlanEntry(l_s[2]))
    # digPlan.append(DigPlanEntry(Direction(l_s[0]), int(l_s[1]), l_s[2]))


def sDigPlan(digPlan):
    s = '\n'
    for entry in digPlan:
        s += str(entry) + '\n'
    return s


debug(sDigPlan(digPlan))


digCount = 0
cX = 0
cY = 0
previousDir = Direction.UNKNOWN
corners = []  # {Coord: corner}
vEdges = []  # {x: edge}
hEdges = []  # {y: edge}
for entry in digPlan:
    digCount += entry.distance
    corner = Corner(Coord(cX, cY), previousDir, entry.direction)
    corners.append(corner)
    nX = cX
    nY = cY
    match entry.direction:
        case Direction.UP: nY -= entry.distance
        case Direction.DOWN: nY += entry.distance
        case Direction.LEFT: nX -= entry.distance
        case Direction.RIGHT: nX += entry.distance
    edge = Edge(Coord(cX, cY), Coord(nX, nY))
    if edge.isVertical:
        vEdges.append(edge)
    else:
        hEdges.append(edge)
    cX = nX
    cY = nY
    previousDir = entry.direction
    if (cX == 0 and cY == 0):
        corners[0].tail = entry.direction

if corners[0].tail == Direction.UNKNOWN:
    raise Exception("loop did not complete")

debug("\n" + str(list(map(lambda corner: f"{corner}", corners))))
debug("\n" + str(list(map(lambda edge: f"{edge}", vEdges))))
debug("\n" + str(list(map(lambda edge: f"{edge}", hEdges))))

count = scancount(corners, vEdges)

debug(count)

print(count)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
