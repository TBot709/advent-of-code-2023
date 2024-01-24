#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
#setDebug(True)

puzzleNumber = "16"
partNumber = "2"

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
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r') # my part 1 answer was 7046
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

def resetCells(cells):
    global lines
    cells = []
    for line in lines:
        lineOfCells = []
        for cellChar in line:
            lineOfCells.append(Cell(cellChar))
        cells.append(lineOfCells)
    return cells

resetCells(cells)

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

def getEnergizedCount(cells):
    numEnergizedTiles = 0
    for line in cells:
        for cell in line:
            if cell.getActiveCount() > 0:
                numEnergizedTiles += 1
    return numEnergizedTiles

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

def jump(beam, cells) -> None:
    dc = beam.directionChar
    offsetX = 1 if dc == EAST else -1 if dc == WEST else 0
    offsetY = 1 if dc == SOUTH else -1 if dc == NORTH else 0
    x = beam.x + offsetX
    y = beam.y + offsetY
    emptyCount = 0
    while y > 0 and x > 0 and y < nRows and x < nColumns and cells[y][x].tileChar == EMPTY:
        emptyCount += 1
        cells[y][x].registerBeam(beam)
        x += offsetX
        y += offsetY
    if emptyCount > 0:
        beam.x = x - offsetX # minus one to get back to first non-empty found
        beam.y = y - offsetY # minus one to get back to first non-empty found

def getEnergizedTileCountForStartingBeam(startingBeam: Beam, cells) -> int:
    cells = resetCells(cells)
    beams = []
    #istartingBeam = Beam(-1, 0, EAST) 
    beams.append(startingBeam)
    while len(beams) > 0:
        for iBeam, beam in enumerate(beams):
            beam.move()

            #debug(f"{beam}")

            if beam.isOutOfBounds():
                #debug(f"popping out of bounds beam, {beam}")
                beams.pop(iBeam)
                continue
            
            cell = cells[beam.y][beam.x]
            
            if cell.isRepeat(beam):
                #debug(f"popping beam on trajectory cell has seen before, {beam}")
                beams.pop(iBeam)
                continue
            
            cell.registerBeam(beam)

            tileChar = cell.tileChar
            #debug(f"{beam.x} {beam.y} {tileChar}")
            if tileChar == EMPTY:
                jump(beam, cells)
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
               
    debug(f"for starting beam, {beam}, energized count, {getEnergizedCount(cells)}: {sCells_active(cells)}")
    return getEnergizedCount(cells)

maxCount = 0

# top side
for i in range(nColumns):
    count = getEnergizedTileCountForStartingBeam(Beam(i, -1, SOUTH), cells)
    if count > maxCount:
        maxCount = count

# right side
for i in range(nRows):
    count = getEnergizedTileCountForStartingBeam(Beam(nColumns + 1, i, WEST), cells)
    if count > maxCount:
        maxCount = count

# bottom side
for i in range(nColumns):
    count = getEnergizedTileCountForStartingBeam(Beam(i, nRows + 1, NORTH), cells)
    if count > maxCount:
        maxCount = count

# left side
for i in range(nRows):
    count = getEnergizedTileCountForStartingBeam(Beam(-1, i, EAST), cells)
    if count > maxCount:
        maxCount = count

print(maxCount)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
