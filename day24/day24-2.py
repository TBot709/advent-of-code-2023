#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug
import math
from lcm import lcm_multiple

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "24"
partNumber = "2"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(),
  # PanicThread.ONE_GIGABYTE,
  PanicThread.FOUR_GIGABYTES,
  # PanicThread.TEN_SECONDS)
  PanicThread.ONE_HOUR)
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

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        elif idx == 1:
            return self.y
        elif idx == 2:
            return self.z
        else:
            raise IndexError("Invalid index for Coord object")


class Vector(Coord):
    pass


class Hailstone:
    def __init__(self, coord: Coord, velocity: Vector):
        self.coord = coord
        self.velocity = velocity
        self.slope2d = velocity.x/velocity.y
        self.slopeX = math.sqrt(velocity.z * velocity.z + velocity.y * velocity.y)/velocity.x
        self.slopeY = math.sqrt(velocity.z * velocity.z + velocity.x * velocity.x)/velocity.y
        self.slopeZ = math.sqrt(velocity.y * velocity.y + velocity.x * velocity.x)/velocity.z
        self.yIntercept = coord.y - self.slope2d * coord.x

    def __str__(self):
        return f"{self.coord} @ {self.velocity}, slope2d: {self.slope2d}, slopeX: {self.slopeX}, slopeY: {self.slopeY}, slopeZ: {self.slopeZ}, yInt: {self.yIntercept}"

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


# cross_product = [vector1[1]*vector2[2] - vector1[2]*vector2[1],
                 # vector1[2]*vector2[0] - vector1[0]*vector2[2],
                 # vector1[0]*vector2[1] - vector1[1]*vector2[0]]
def crossProduct(v1: Vector, v2: Vector):
    return (v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x)

def intersect3d(hsA, hsB, prec=1e-6):
    # Unpack line parameters
    (x1, y1, z1), (a, b, c) = (
            (hsA.coord.x, hsA.coord.y, hsA.coord.z),
            (hsA.velocity.x, hsA.velocity.y, hsA.velocity.z))
    (x2, y2, z2), (p, q, r) = (
            (hsB.coord.x, hsB.coord.y, hsB.coord.z),
            (hsB.velocity.x, hsB.velocity.y, hsB.velocity.z))

    # Calculate denominator
    denom = a*q - b*p

    # If the denominator is zero, lines are parallel and do not intersect
    if denom == 0:
        return None

    # Calculate t1 and t2
    t1 = ((x2-x1)*q - (y2-y1)*p) / denom
    t2 = ((x2-x1)*b - (y2-y1)*a) / denom

    # Calculate intersection point
    x = x1 + a*t1
    y = y1 + b*t1
    z = z1 + c*t1

    # debug(f"{(x1, y1, z1)}, {(a, b, c)}, {(x2, y2, z2)}, {(p, q, r)}, {denom}, {x}, {y}, {z}, {abs(x - (x2 + p*t2))}, {abs(y - (y2 + q*t2))}, {abs(z - (z2 + r*t2))}")

    # Check if intersection point lies on both lines
    if abs(x - (x2 + p*t2)) < prec and abs(y - (y2 + q*t2)) < prec and abs(z - (z2 + r*t2)) < prec:
        return (x, y, z)

    # If not, lines do not intersect
    return None


# a Plane can be defined that any two hailstone trajectories lie on
class Plane:

    # given parametetric form of trajectory lines,
    #  (x - x0)/vx = (y - y0)/vy = (z - z0)/vz
    # and the normal from the cross product of the two velocity vectors,
    #  v1 cross v2 = (a, b, c)
    # and the intersection (xI, yI, zI)
    # we can derive a plane equation,
    #  a*(x - xI) + b*(y - yI) + c*(z - zI) = 0
    def __init__(self, hsA, hsB):
        self.normal = crossProduct(hsA.velocity, hsB.velocity)
        # debug(self.normal)
        self.intersection = intersect3d(hsA, hsB)
        # debug(self.intersection)
        # get lcd for normal points
        # lcm = lcm_multiple(self.normal)
        # for i, n in enumerate(self.normal):
            # self.normal[i] = n/lcm
        # debug(self.normal)


PRECISION = 1e-5
# PRECISION = 1e-10


def areParallel3d(hsA, hsB):
    return (
            math.isclose(hsA.slopeX, hsB.slopeX, rel_tol=PRECISION)  and
            math.isclose(hsA.slopeY, hsB.slopeY, rel_tol=PRECISION) and
            math.isclose(hsA.slopeZ, hsB.slopeZ, rel_tol=PRECISION))


hailstones = []
for line in lines:
    splitLine = line.split('@')
    splitCoord = splitLine[0].split(',')
    splitVelocity = splitLine[1].split(',')
    hailstone = Hailstone(
            Coord(splitCoord[0], splitCoord[1], splitCoord[2]),
            Vector(splitVelocity[0], splitVelocity[1], splitVelocity[2]))
    # debug(hailstone)
    hailstones.append(hailstone)

# for i, hsA in enumerate(hailstones):
    # for hsB in hailstones[(i + 1):]:
        # debug(f"\n{hsA}\n{hsB}\n\tareParallel = {areParallel3d(hsA, hsB)}")
        # if areParallel3d(hsA, hsB):
            # debug(f"PARALLEL!\n{hsA}\n{hsB}")
        # Plane(hsA, hsB)



def plot():
    import matplotlib.pyplot as plt
    import numpy as np

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot_min = 10000000000000
    plot_max = 500000000000000
    ax.set_xlim([plot_min, plot_max])
    ax.set_ylim([plot_min, plot_max])
    ax.set_zlim([plot_min, plot_max])

    # Plot the trajectory of each projectile
    for hs in hailstones:
        # Extract the initial position and velocity
        x0, y0, z0 = hs.coord
        vx, vy, vz = hs.velocity

        debug(f"plotting {x0}, {y0}, {z0}, {vx}, {vy}, {vz}")

        # Create an array of time values
        t = np.linspace(0, 1000000000000, num=100)

        # Calculate the trajectory
        x = x0 + vx * t
        y = y0 + vy * t
        z = z0 + vz * t

        # Plot the trajectory
        ax.plot(x, y, z)

    # Set the labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Projectile Trajectories')

    # Display the plot
    plt.show()


# plot()


## attempts to narrow down:
# line 337: 72 intersects for (160000000000000, 231000000000000, 219000000000000), (73, 25, 51)


# search space
# ssxStart = 100000000000000
# ssxEnd = 200000000000000
ssxStart = 160000000000000
ssxEnd = 161000000000000
ssxMid = ssxStart + (ssxEnd - ssxStart)/2
# ssyStart = 150000000000000
# ssyEnd = 250000000000000
ssyStart = 230000000000000
ssyEnd = 232000000000000
ssyMid = ssyStart + (ssyEnd - ssyStart)/2
# sszStart = 150000000000000
# sszEnd = 250000000000000
sszStart = 218000000000000
sszEnd = 220000000000000
sszMid = sszStart + (sszEnd - sszStart)/2


def closestToOrigin(hsA, hsB):
    hsAx, hsAy, hsAz = hsA.coord
    hsBx, hsBy, hsBz = hsB.coord
    return math.hypot(hsAx, hsAy, hsAz) - math.hypot(hsBx, hsBy, hsBz)


from functools import cmp_to_key

sortedHailstones = sorted(hailstones, key=cmp_to_key(closestToOrigin))

debug(sortedHailstones[0])

solutionCoords = None
solutionVelocity = None
isSolutionFound = False
# # # # 1234567890123
step = 100000000000
# step = 10000000000000
# # # # # #  1234567890123
precision = 10000000000
# precision = 1000000000000
intersectCountDisplayLimit = 1
# vStart = 0
# vEnd = 80
vxStart = 60
vxEnd = 80
vyStart = 10
vyEnd = 30
vzStart = 40
vzEnd = 60
testCount = 0
x = ssxStart - step
while x <= ssxEnd and not isSolutionFound:
    x += step
    y = ssyStart - step
    while y <= ssyEnd - step and not isSolutionFound:
        y += step
        z = sszStart - step
        while z <= sszEnd - step and not isSolutionFound:
            z += step
            # if testCount % 100000 == 0:
                # debug(f"({x}, {y}, {z})")
            # debug(f"({x}, {y}, {z})")
            vx = vxStart - 1
            while vx <= (vxEnd - 1) and not isSolutionFound:
                vx += 1
                vy = vyStart - 1
                while vy <= (vyEnd - 1) and not isSolutionFound:
                    vy += 1
                    vz = vzStart - 1
                    while vz <= (vzEnd - 1) and not isSolutionFound:
                        vz += 1
                        testCount += 1
                        if testCount % 1000000 == 0:
                            debug(f"({x}, {y}, {z}), ({vx}, {vy}, {vz})")
                        # debug(f"({x}, {y}, {z}), ({vx}, {vy}, {vz})")
                        testHailstone = Hailstone(
                            Coord(x, y, z),
                            Vector(vx, vy, vz))
                        isAllIntersect = True
                        intersectCount = 0
                        for hs in sortedHailstones:
                            intersect = intersect3d(testHailstone, hs, precision)
                            if intersect is None:
                                isAllIntersect = False
                                break
                            if not hs.isPointInFuture(
                                    Coord(
                                        intersect[0],
                                        intersect[1],
                                        intersect[2])):
                                isAllIntersect = False
                                break
                            intersectCount += 1
                        if intersectCount > intersectCountDisplayLimit:
                            debug(f"{intersectCount} intersects for ({x}, {y}, {z}), ({vx}, {vy}, {vz})")
                        if isAllIntersect:
                            solutionCoords = (x, y, z)
                            solutionVelocity = (vx, vy, vz)
                            isSolutionFound = True

debug(f"{solutionCoords}, {solutionVelocity}")

print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
