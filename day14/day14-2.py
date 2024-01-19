#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)

puzzleNumber = "14"
partNumber = "2"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  #  PanicThread.TEN_SECONDS)
  PanicThread.ONE_HOUR)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
#file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input-2.txt",'r')
#file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input.txt",'r')
#file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
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
    for iRow, row in enumerate(grid):
        for iColumn, c in enumerate(row):
#            debug(f"rollN: {iRow} {iColumn} {grid[iRow][iColumn]}") 
            if c == ROLLER:
                rollDistance = 0
                currentCell = grid[iRow - 1][iColumn]
                while iRow - rollDistance > 0 and currentCell == EMPTY:
#                    debug(f"\t{iRow - (1 + rollDistance)} {iColumn} {currentCell}")
                    rollDistance += 1
                    currentCell = grid[iRow - (1 + rollDistance)][iColumn]
                if rollDistance > 0:
#                    debug(f"\tmoving {ROLLER} from row {iRow} column {iColumn} to row {iRow - rollDistance}")
                    grid[iRow][iColumn] = EMPTY
                    grid[iRow - rollDistance][iColumn] = ROLLER

def rollW(grid):
    for iRow, row in enumerate(grid):
        for iColumn, c in enumerate(row):
#            debug(f"rollW: {iRow} {iColumn} {grid[iRow][iColumn]}") 
            if c == ROLLER:
                rollDistance = 0
                currentCell = grid[iRow][iColumn - 1]
                while iColumn - rollDistance > 0 and currentCell == EMPTY:
#                    debug(f"\t{iRow} {iColumn - (1 + rollDistance)} {currentCell}")
                    rollDistance += 1
                    currentCell = grid[iRow][iColumn - (1 + rollDistance)]
                if rollDistance > 0:
#                    debug(f"\tmoving {ROLLER} from row {iRow} column {iColumn} to column {iColumn - rollDistance}")
                    grid[iRow][iColumn] = EMPTY
                    grid[iRow][iColumn - rollDistance] = ROLLER
 
def rollS(grid):
    iRow = len(grid) - 2 
    while iRow >= 0:
        row = grid[iRow]
        for iColumn, c in enumerate(row):
#            debug(f"rollN: r{iRow} c{iColumn} {grid[iRow][iColumn]}") 
            if c == ROLLER:
                rollDistance = 0
                currentCell = grid[iRow + 1][iColumn]
                while currentCell == EMPTY:
#                    debug(f"\tr{iRow + 1 + rollDistance} c{iColumn} roll{rollDistance} {currentCell}")
                    rollDistance += 1
                    if iRow + 1 + rollDistance < len(grid):
                        currentCell = grid[iRow + 1 + rollDistance][iColumn]
                    else:
                        break
                if rollDistance > 0:
#                    debug(f"\tmoving {ROLLER} from row {iRow} column {iColumn} to row {iRow + rollDistance}")
                    grid[iRow][iColumn] = EMPTY
                    grid[iRow + rollDistance][iColumn] = ROLLER
        iRow -= 1

def rollE(grid):
    for iRow, row in enumerate(grid):
        iColumn = len(row) - 2
        while iColumn >= 0:
            c = row[iColumn]
#            debug(f"rollW: {iRow} {iColumn} {grid[iRow][iColumn]}") 
            if c == ROLLER:
                rollDistance = 0
                currentCell = grid[iRow][iColumn + 1]
                while currentCell == EMPTY:
#                    debug(f"\t{iRow} {iColumn + 1 + rollDistance} {currentCell}")
                    rollDistance += 1
                    if iColumn + 1 + rollDistance < len(row):
                        currentCell = grid[iRow][iColumn + 1 + rollDistance]
                    else:
                        break
                if rollDistance > 0:
#                    debug(f"\tmoving {ROLLER} from row {iRow} column {iColumn} to column {iColumn - rollDistance}")
                    grid[iRow][iColumn] = EMPTY
                    grid[iRow][iColumn + rollDistance] = ROLLER
            iColumn -= 1

def isCyclingValues(l: list) -> bool:
    n = len(l)
    for cycle_length in range(1, n):
        if n % cycle_length == 0:
            segment = l[:cycle_length]
            if all(l[i:i+cycle_length] == segment for i in range(cycle_length, n, cycle_length)):
                return True
    return False

def getTotalLoad(grid):
    totalLoad = 0
    for iRow, row in enumerate(grid):
        rowLeverage = len(grid) - iRow
        for iColumn, c in enumerate(row):
            if c == ROLLER:
                totalLoad += rowLeverage
    return totalLoad

debug(f"before rolling: {sGrid(grid)}")

nCycles = 1000000000
#nCycles = 3 
rollFunctions = [rollN, rollW, rollS, rollE]
nRollFunctions = len(rollFunctions)
gridHashRecord = []
iRolls = 0
iCycles = 0
iRollFunction = 0
isCycling = False
potentialCycle = () # (hash, iRolls, potentialPeriod)
while iCycles <= nCycles:
    rollFunctions[iRollFunction](grid)
    debug(f"roll {iRolls + 1}, rollFunction {iRollFunction}, cycle {iCycles}")
    debug(f"\ttotal load = {getTotalLoad(grid)}")
    iRollFunction += 1
    if iRollFunction > nRollFunctions - 1:
        iCycles += 1
        iRollFunction = 0

    h = hash(sGrid(grid) + str(iRollFunction))
    if not isCycling and (h in gridHashRecord):
        debug(f"\tPOTENTIAL CYCLE: {iCycles} {h}")
        if potentialCycle == ():
            potentialCycle = (h, iRolls, 0)
            debug(f"\t\tCYCLE CANDIDATE: {potentialCycle}")
        else:
            if h == potentialCycle[0]:
                if potentialCycle[2] == 0:
                    potentialCycle = (h, iRolls, iRolls - potentialCycle[1])
                    debug(f"\t\tCYCLE CANDIDATE PERIOD DETERMINED: {potentialCycle}")
                else:
                    if potentialCycle[2] == iRolls - potentialCycle[1]:
                        isCycling = True
                        iCycles = nCycles - ((nCycles*len(rollFunctions) - iRolls)%potentialCycle[2])//len(rollFunctions)
                        debug(f"\t\tCYCLE CANDIDATE PERIOD CONFIRMED: {potentialCycle}, jumping to cycle {iCycles}")
                    else: 
                        debug(f"\t\tCYCLE CANDIDATE REJECTED: {potentialCycle}")
                        potentialCycle = ()

    iRolls += 1
    gridHashRecord.append(h)
#    if not isCycling and isCyclingValues(gridHashRecord[-1000::]):
#        isCycling = True
#        nCycles = (nCycles - iRolls) % len(rollFunctions) 
#        iRolls = 0
#        debug(f"found cycle {nCycles} {gridHashRecord[-1000::]}")

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
