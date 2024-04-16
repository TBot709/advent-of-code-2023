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

grid = []
for line in lines:
    row = []
    for c in line:
        row.append(c)
    grid.append(row)

def strGrid():
    s += "\n"
    for row in grid:
        for c in row:
            s += c
        s += "\n"
    return s

debug(strGrid())

SLOPE_N = '^'
SLOPE_W = '<'
SLOPE_E = '>'
SLOPE_S = 'v'

class Node:
    def __init__(self, coord, srcSlope):
        self.coord = coord
        self.srcSlope = srcSlope
        self.explored 

endNode = Node((nColumns - 1, nRows), None)

nodes = [Node((1, 0), None))
currentNode = (1, 0)
c: = (1, 1)
while grid[c[1]][c[0]] not in [SLOPE_N, SLOPE_W, SLOPE_E, SLOPE_S]:


print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
