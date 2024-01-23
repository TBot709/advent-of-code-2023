#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)

puzzleNumber = "16"
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

class Cell:
    # Cell(".") 
    def __init__(self, tileChar):
        self.tileChar = tileChar
        self.activeCount = 0

NORTH = "N"
EAST = "E"
SOUTH = "S"
WEST = "W"
class Beam:
    # Beam(0, 0, "E")
    def __init__(self, x, y, directionChar):
        self.x = x
        self.y = y
        self.directionChar = directionChar
    def move(self):
        if directionChar == NORHT:
            self.y -= 1
        elif directionChar == EAST:
            self.x += 1
        elif directionChar == SOUTH:
            self.y += 1
        elif directionChar == WEST:
            self.x -= 1
    def isOutOfBounds(self):
        return self.x < 0 or self.y < 0 or \
                self.x > nColumns or self.y > nRows

cells = []
for line in lines:
    lineOfCells = []
    for cellChar in line:
        lineOfCells.append(Cell(cellChar))
    cells.append(lineOfCells)

def sCells(cells) -> str:
    s = "\n"
    for line in cells:      
        for cell in line:
            s += f"{cell.tileChar}"
        s += "\n"
    return s

debug(sCells(cells))     

beams = []
beams.append(Beam(0, 0, EAST))
while len(beams) > 0:
    for iBeam, beam in enumerate(beams):
        cells[beam.x][beam.y].activeCount += 1
        tileChar = cells[beam.x][beam.y].tileChar
        if tileChar = ".":
            beam.move()    
        elif tileChar = 
        if beam.isOutOfBounds:
            beams.pop(iBeam)

print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
