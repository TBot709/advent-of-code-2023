#!/usr/bin/python

import sys
import threading
# import resource
import heapq
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)

puzzleNumber = "17"
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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_simple-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_extra-short-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # #  Running solution for day{puzzleNumber}-{partNumber}  # # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

# build integer grid from input
grid = []  # grid[iLine][iC]
for line in lines:
    gridLine = []
    for c in line:
        gridLine.append(int(c))
    grid.append(gridLine)


def sGrid(grid) -> str:
    s = "\n"
    for line in grid:
        for c in line:
            s += str(c)
        s += "\n"
    return s


debug(sGrid(grid))

MAX_JUMP = 3
adjMatrix = {}
for iLine, line in enumerate(grid):
    for iCell, cell in enumerate(line):
        cell = (iCell, iLine)
        if cell not in adjMatrix:
            adjMatrix[cell] = {}
        # for every cell in vertical line, MAX_JUMP above
        cost = 0
        for i in range(MAX_JUMP):
            iAdj = iLine - 1 - i
            if iAdj < 0 or iAdj >= nRows:
                continue
            adjCell = (iCell, iAdj)
            cost += grid[iAdj][iCell]
            adjMatrix[cell][adjCell] = cost
        # for every cell in vertical line, MAX_JUMP below
        cost = 0
        for i in range(MAX_JUMP):
            iAdj = iLine + 1 + i
            if iAdj < 0 or iAdj >= nRows:
                continue
            adjCell = (iCell, iAdj)
            cost += grid[iAdj][iCell]
            adjMatrix[cell][adjCell] = cost
        # for every cell in horizontal line, MAX_JUMP left
        cost = 0
        for i in range(MAX_JUMP):
            iAdj = iCell - 1 - i
            if iAdj < 0 or iAdj >= nColumns:
                continue
            adjCell = (iAdj, iLine)
            cost += grid[iLine][iAdj]
            adjMatrix[cell][adjCell] = cost
        # for every cell in horizontal line, MAX_JUMP right
        cost = 0
        for i in range(MAX_JUMP):
            iAdj = iCell + 1 + i
            if iAdj < 0 or iAdj >= nColumns:
                continue
            adjCell = (iAdj, iLine)
            cost += grid[iLine][iAdj]
            adjMatrix[cell][adjCell] = cost

NORTH = '^'
EAST = '>'
SOUTH = 'v'
WEST = '<'


def getDistanceAndDirection(firstXYTuple, secondXYTuple):
    relativeX = secondXYTuple[0] - firstXYTuple[0]
    relativeY = secondXYTuple[1] - firstXYTuple[1]

    if relativeX > 0:
        direction = EAST
    elif relativeX < 0:
        direction = WEST
    elif relativeY > 0:
        direction = SOUTH
    else:
        direction = NORTH

    if direction == EAST or direction == WEST:
        distance = relativeX
    else:
        distance = relativeY

    if distance < 0:
        distance *= -1

    return (distance, direction)


class PathNode:
    def __init__(self, x, y, prevDirection, prevJumpDist):
        self.x = x
        self.y = y
        self.prevDirection = prevDirection
        self.prevJumpDist = prevJumpDist

    def __eq__(self, other):
        return self.x == other.x and \
                self.y == other.y and \
                self.prevDirection == other.prevDirection and \
                self.prevJumpDist == other.prevJumpDist

    def __hash__(self):
        return hash(str(self.x) + "," +
                    str(self.y) + "," +
                    self.prevDirection + "," +
                    str(self.prevJumpDist))

    def __lt__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __str__(self):
        return f"({self.x}, {self.y}, {self.prevDirection}, {self.prevJumpDist})"


def dijkstra(adj_list, start):
    # rtrn = {PathNode: (distance, prevNode)}
    rtrn = {}
    for node in adj_list:
        for x in range(3):
            rtrn[PathNode(node[0], node[1], NORTH, x + 1)] = (float('inf'), None)
            rtrn[PathNode(node[0], node[1], EAST, x + 1)] = (float('inf'), None)
            rtrn[PathNode(node[0], node[1], SOUTH, x + 1)] = (float('inf'), None)
            rtrn[PathNode(node[0], node[1], WEST, x + 1)] = (float('inf'), None)

    # debug(list(map(lambda n: str(n), rtrn)))

    startNode = PathNode(start[0], start[1], NORTH, 0)
    rtrn[startNode] = (0, None)

    # priority_queue = [(distance, node)]
    priority_queue = [(0, startNode)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # debug(f"{current_distance}, {current_node}")

        if current_distance > rtrn[current_node][0]:
            continue

        for neighbor, weight in adj_list[(current_node.x, current_node.y)].items():
            distanceAndDirection = \
                    getDistanceAndDirection(
                        (current_node.x, current_node.y),
                        neighbor)
            # debug(f"\t{neighbor}, {distanceAndDirection}")
            # skip if direction to this neighbour matched previous jump direction
            if distanceAndDirection[1] == current_node.prevDirection:
                continue

            # skip if diretion to neighbor is opposite previous direction
            elif distanceAndDirection[1] == NORTH and current_node.prevDirection == SOUTH or \
                    distanceAndDirection[1] == EAST and current_node.prevDirection == WEST or \
                    distanceAndDirection[1] == SOUTH and current_node.prevDirection == NORTH or \
                    distanceAndDirection[1] == WEST and current_node.prevDirection == EAST:
                continue

            distance = current_distance + weight
            neighborNode = \
                PathNode(
                    neighbor[0],
                    neighbor[1],
                    distanceAndDirection[1],
                    distanceAndDirection[0])
            # debug(f"\t{neighborNode}")
            neighborDistance = rtrn[neighborNode][0]
            # If shorter path to neighbor is found, update distance and push to queue
            if distance < neighborDistance:
                rtrn[neighborNode] = (distance, current_node)
                heapq.heappush(priority_queue, (distance, neighborNode))
    return rtrn


def sDijkstraReturn(d):
    if not d:
        return "The dictionary is empty."

    min_x = min(n.x for n in d.keys())
    max_x = max(n.x for n in d.keys())
    min_y = min(n.y for n in d.keys())
    max_y = max(n.y for n in d.keys())

    s = "\n"
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            s += "["
            for direction in [NORTH, EAST, SOUTH, WEST]:
                for dist in range(1, 4):
                    node = PathNode(x, y, direction, dist)
                    shortestPathDist = d[node]
                    if shortestPathDist == float('inf'):
                        shortestPathDist = -1
                    s += f"{direction}{dist}:{shortestPathDist},"
            s += "] "
        s += '\n'
    return s


def sDijkstraReturn_pathOnly(d):
    if not d:
        return "The dictionary is empty."

    min_x = min(n.x for n in d.keys())
    max_x = max(n.x for n in d.keys())
    min_y = min(n.y for n in d.keys())
    max_y = max(n.y for n in d.keys())

    def shortestAtCoords(coords, d):
        shortestNode = None
        shortest = float('inf')
        for direction in [NORTH, EAST, SOUTH, WEST]:
            for dist in range(1, 4):
                node = PathNode(coords[0], coords[1], direction, dist)
                if d[node][0] < shortest:
                    shortestNode = node
                    shortest = d[node][0]
        return shortestNode

    finalNode = shortestAtCoords((max_x, max_y), d)

    path = [finalNode]
    while d[path[-1]][1] is not None:
        path.append(d[path[-1]][1])

    debug(list(map(lambda node: str(node), path)))

    s = "\n"
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            pathNode = next((node for node in path if node.x == x and node.y == y), None)
            if pathNode is not None:
                s += pathNode.prevDirection
            else:
                s += str(grid[y][x])
        s += '\n'
    return s


d = dijkstra(adjMatrix, (0, 0))

# debug(adjMatrix)
# debug(d)
# debug(list(map(lambda kv: str(kv[0]) + ":" + str(kv[1]) if kv[1] < 9999 else "", d.items())))
# debug(list(map(lambda kv: str(kv[0]) + ":" + str(kv[1][0]), d.items())))
# debug(sDijkstraReturn(d))
debug(sDijkstraReturn_pathOnly(d))

minDist = float('inf')
endX = nColumns - 1
endY = nRows - 1
for x in range(3):
    dN = d[PathNode(endX, endY, NORTH, x + 1)][0]
    dE = d[PathNode(endX, endY, EAST, x + 1)][0]
    dS = d[PathNode(endX, endY, SOUTH, x + 1)][0]
    dW = d[PathNode(endX, endY, WEST, x + 1)][0]
    minDist = dN if dN < minDist else minDist
    minDist = dE if dE < minDist else minDist
    minDist = dS if dS < minDist else minDist
    minDist = dW if dW < minDist else minDist

print(minDist)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
