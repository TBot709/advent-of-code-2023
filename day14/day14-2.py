#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)

puzzleNumber = "14"
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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # #  Running solution for day{puzzleNumber}-{partNumber}  # # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

EMPTY = '.'
ROLLER = 'O'
CUBE = '#'

grid = []
for line in lines:
    gridLine = []
    for c in line:
        gridLine.append(c)
    grid.append(gridLine)

def sGrid(grid):
    s = "\n"
    for row in grid:
        for c in row:
            s += c
        s += '\n'
    return s

def rollN(grid):
    iRow = 1
    for row in grid[1::]:
        for iColumn, c in enumerate(row):
    #        debug(f"{iRow} {iColumn} {grid[iRow][iColumn]}") 
            if c == ROLLER:
                rollDistance = 0
                currentCell = grid[iRow - 1][iColumn]
                while iRow - rollDistance > 0 and currentCell == EMPTY:
    #                debug(f"\t{iRow - (1 + rollDistance)} {iColumn} {currentCell}")
                    rollDistance += 1
                    currentCell = grid[iRow - (1 + rollDistance)][iColumn]
                if rollDistance > 0:
    #                debug(f"\tmoving {ROLLER} from row {iRow} column {iColumn} to row {iRow - rollDistance}")
                    grid[iRow][iColumn] = EMPTY
                    grid[iRow - rollDistance][iColumn] = ROLLER
        iRow += 1

debug(f"before rolling: {sGrid(grid)}")

gridHashRecord = []
for i in range(10): 
    gridHashRecord.append(hash(sGrid(grid)))
    rollN(grid)

debug(f"after rolling: {sGrid(grid)}")

totalLoad = 0

for iRow, row in enumerate(grid):
    rowLeverage = len(grid) - iRow
    for iColumn, c in enumerate(row):
        if c == ROLLER:
            totalLoad += rowLeverage

print(totalLoad)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
