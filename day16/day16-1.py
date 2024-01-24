#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
#setDebug(True)

puzzleNumber = "16"
partNumber = "1"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  #PanicThread.TEN_SECONDS)
  PanicThread.ONE_HOUR)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
#file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
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
        if self.directionChar == NORTH:
            self.y -= 1
        elif self.directionChar == EAST:
            self.x += 1
        elif self.directionChar == SOUTH:
            self.y += 1
        elif self.directionChar == WEST:
            self.x -= 1
    def isOutOfBounds(self):
        return self.x < 0 or self.y < 0 or \
                self.x >= nColumns or self.y >= nRows
    def __str__(self):
        return f"({self.x}, {self.y}, {self.directionChar})"

class Cell:
    # Cell(".") 
    def __init__(self, tileChar):
        self.tileChar = tileChar
        self._isActive = [False, False, False, False] # [N, E, S, W]
    def registerBeam(self, beam: Beam) -> None:
        dc = beam.directionChar
        if dc == NORTH: self._isActive[0] = True
        if dc == EAST: self._isActive[1] = True
        if dc == SOUTH: self._isActive[2] = True
        if dc == WEST: self._isActive[3] = True
    def getActiveCount(self) -> int:
        return self._isActive.count(True)
    def isRepeat(self, beam: Beam) -> bool:
        dc = beam.directionChar
        return (dc == NORTH and self._isActive[0]) or \
                (dc == EAST and self._isActive[1]) or \
                (dc == SOUTH and self._isActive[2]) or \
                (dc == WEST and self._isActive[3])

cells = [] # cells[cell.y][cell.x]
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

def sCells_active(cells) -> str:
    s = "\n"
    for line in cells:
        for cell in line:
            if cell.getActiveCount() > 0:
                s += str(cell.getActiveCount())
            else:
                s += cell.tileChar
        s += "\n"
    return s

debug(sCells(cells))     

EMPTY = "."
M_BACKSLASH = "\\"
M_FORWARDSLASH = "/"
S_HORIZONTAL = "-"
S_VERTICAL = "|"

def getMBackslashDirectionCompliment(directionChar):
    if directionChar == NORTH: return WEST
    if directionChar == EAST: return SOUTH
    if directionChar == SOUTH: return EAST
    if directionChar == WEST: return NORTH

def getMForwardSlashDirectionCompliment(directionChar):
    if directionChar == NORTH: return EAST
    if directionChar == EAST: return NORTH
    if directionChar == SOUTH: return WEST
    if directionChar == WEST: return SOUTH

beams = []
startingBeam = Beam(-1, 0, EAST) 
beams.append(startingBeam)
while len(beams) > 0:
    for iBeam, beam in enumerate(beams):
        beam.move()

        debug(f"{beam}")

        if beam.isOutOfBounds():
            debug(f"popping out of bounds beam, {beam}")
            beams.pop(iBeam)
            continue
        
        cell = cells[beam.y][beam.x]
        
        if cell.isRepeat(beam):
            debug(f"popping beam on trajectory cell has seen before, {beam}")
            beams.pop(iBeam)
            continue
        
        cell.registerBeam(beam)

        tileChar = cell.tileChar
        debug(f"{beam.x} {beam.y} {tileChar}")
        if tileChar == EMPTY:
            # nothing
            pass
        elif tileChar == M_BACKSLASH:
            beam.directionChar = getMBackslashDirectionCompliment(beam.directionChar)
        elif tileChar == M_FORWARDSLASH:
            beam.directionChar = getMForwardSlashDirectionCompliment(beam.directionChar)
        elif tileChar == S_VERTICAL:
            if beam.directionChar == EAST or beam.directionChar == WEST:
                beam.directionChar = NORTH
                beams.append(Beam(beam.x, beam.y, SOUTH))
        elif tileChar == S_HORIZONTAL:
            if beam.directionChar == NORTH or beam.directionChar == SOUTH:
                beam.directionChar = EAST
                beams.append(Beam(beam.x, beam.y, WEST))
        else:
            raise Exception(f"unhandled tileChar, {tileChar}")
           
        debug(sCells_active(cells))

print(sCells_active(cells))

numEnergizedTiles = 0
for line in cells:
    for cell in line:
        if cell.getActiveCount() > 0:
            numEnergizedTiles += 1

print(numEnergizedTiles)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
