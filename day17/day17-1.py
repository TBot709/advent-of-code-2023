#!/usr/bin/python

import sys
import threading
import resource
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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_extra-short-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
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

import heapq
def dijkstra(adj_list, start):
    rtrn = {node: (float('inf'), (-1,-1)) for node in adj_list}
    rtrn[start] = (0, start)

    # Priority queue to track nodes and current shortest distance
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the smallest distance from the priority queue
        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip if a shorter distance to current_node is already found
        if current_distance > rtrn[current_node][0]:
            continue

        # Explore neighbors and update rtrn if a shorter path is found
        for neighbor, weight in adj_list[current_node].items():
            distance = current_distance + weight

            # If shorter path to neighbor is found, update distance and push to queue
            if distance < rtrn[neighbor][0]:
                rtrn[neighbor] = (distance, current_node)
                heapq.heappush(priority_queue, (distance, neighbor))
    return rtrn

def sDijkstraReturn(d):
    if not d:
        return "The dictionary is empty."

    min_x = min(x for x, y in d.keys())
    max_x = max(x for x, y in d.keys())
    min_y = min(y for x, y in d.keys())
    max_y = max(y for x, y in d.keys())

    s = "\n"
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            s += f"[({x}, {y}), " + str(d.get((x, y), '#')) + '] '
        s += '\n'
    return s

d = dijkstra(adjMatrix, (0, 0))

debug(adjMatrix)
debug(d)
debug(sDijkstraReturn(d))

minHeatLoss = d[(nColumns - 1, nRows - 1)][0]

print(minHeatLoss)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print(f"peak memory: {peakMemory}")
panic_thread.end()
