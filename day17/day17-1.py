#!/usr/bin/python

import sys
import threading
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
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
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
grid = [] # grid[iLine][iC]
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

adjMatrix = {}
for iLine, line in enumerate(grid):
  for iCell, cell in enumerate(line):
    cell = (iCell, iLine)
    if cell not in adjMatrix:
      adjMatrix[cell] = {}
    # for every cell in vertical line, 3 above, 3 below
    for iAdjVertical in range(iLine - 3, iLine + 3):
      if iAdjVertical < 0 or iAdjVertical >= nRows:
        continue
      adjCell = (iCell, iAdjVertical)
      grid[iAdjVetical][iCell]
      #if adjCell not in adjMatrix:
      #  adjMatrix[adjCell] = {}

      


print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
