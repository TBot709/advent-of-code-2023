#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "24"
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


class Coord:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


class Vector(Coord):
    pass


class Hailstone:
    def __init__(self, coord: Coord, velocity: Vector):
        self.coord = coord
        self.velocity = velocity
        self.slope2d = velocity.y/velocity.x
        self.yIntercept = coord.y - self.slope2d * coord.x

    def __str__(self):
        return f"{self.coord} @ {self.velocity}, slope: {self.slope2d}, yInt: {self.yIntercept}"

    # eq of motion x(t) = x(0) + vx * t, so t = (x(t) - x(0))/vx
    def isPointInFuture(self, point: Coord):
        if point is None:
            return False
        t = (point.x - self.coord.x)/self.velocity.x
        return t > 0


# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
# given hailstoneA: y = ax + c, hailstoneB: y = bx + d
# intersect point: p = ((d - c)/(a - b), a*((d - c)/(a - b)) + c)
# slopeDiff = (a - b), intersectDiff = (d - c)
def getIntersectionPoint(hailstoneA, hailstoneB) -> Coord:
    slopeDiff = hailstoneA.slope2d - hailstoneB.slope2d
    if slopeDiff == 0:
        return None
    intersectDiff = hailstoneB.yIntercept - hailstoneA.yIntercept
    intersectOverSlopeDiff = intersectDiff / slopeDiff
    return Coord(
            intersectOverSlopeDiff,
            hailstoneA.slope2d*intersectOverSlopeDiff + hailstoneA.yIntercept,
            0)


hailstones = []
for line in lines:
    splitLine = line.split('@')
    splitCoord = splitLine[0].split(',')
    splitVelocity = splitLine[1].split(',')
    hailstone = Hailstone(
            Coord(splitCoord[0], splitCoord[1], splitCoord[2]),
            Vector(splitVelocity[0], splitVelocity[1], splitVelocity[2]))
    debug(hailstone)
    hailstones.append(hailstone)

rangeMin = 200000000000000  # 7
rangeMax = 400000000000000  # 27
futureIntersectCount = 0

for i, hsA in enumerate(hailstones):
    for hsB in hailstones[(i + 1):]:
        intersect = getIntersectionPoint(hsA, hsB)
        isInRange = (
                intersect is not None and
                intersect.x >= rangeMin and
                intersect.x <= rangeMax and
                intersect.y >= rangeMin and
                intersect.y <= rangeMax)
        isInFuture = (
                hsA.isPointInFuture(intersect) and
                hsB.isPointInFuture(intersect))

        if isInRange and isInFuture:
            futureIntersectCount += 1

        # debug(f"\n{hsA}\n{hsB}\n\t\t{intersect}\n\t\tisInRange = {isInRange}\n\t\tisInFuture = {isInFuture}")

print(futureIntersectCount)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
