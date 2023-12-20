#!/usr/bin/python

import sys
import threading
import inspect
from datetime import datetime
from panic_thread import PanicThread

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  PanicThread.TEN_SECONDS)
panic_thread.start()

# debug print method
DEBUG = False
DEBUG = True
def debug(msg) -> None:
  if DEBUG:
    lineno = str(inspect.stack()[1].lineno)
    label = "line    "
    labelWithLineno = label[0:len(label) - len(lineno)] + lineno
    print(f"{labelWithLineno}: {msg}")
start = datetime.now()

# get input lines
puzzleNumber = "10"
# file = open(f"day{puzzleNumber}_example-input-1.txt",'r')
# file = open(f"day{puzzleNumber}_example-input-2.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-1.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-1-alt.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-1-alt-rotated.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-2.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-3.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-4.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-5.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-6.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-7.txt",'r')
# file = open(f"day{puzzleNumber}-2_example-input-8.txt",'r')
file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

from coord import Coord
from enum import Enum

Direction = Enum('Direction', ['N','W','E','S'])

def getCoordIfInBounds(x: int, y: int):
  if x < 0 or x >= nColumns or y < 0 or y >= nRows:
    return None
  return Coord(x, y)

class Tile:
  directions: list[Direction] = []
  symbol = "."
  distance = None
  isPartOfLoop = False
  isInside = False
  def __init__(self, coord: Coord):
    self.coord = coord
    self.adjacentCoordN = getCoordIfInBounds(coord.x, coord.y - 1)
    self.adjacentCoordW = getCoordIfInBounds(coord.x - 1, coord.y)
    self.adjacentCoordE = getCoordIfInBounds(coord.x + 1, coord.y)
    self.adjacentCoordS = getCoordIfInBounds(coord.x, coord.y + 1)
  def __str__(self):
    return f"{self.symbol}@[{self.coord.x},{self.coord.y}]"
  def getConnectingTiles(self, map: dict[Coord, "Tile"]) -> dict["Tile"]:
    r = []
    for d in self.directions:
      match d:
        case Direction.N:
          if self.adjacentCoordN is not None:
            other = map[self.adjacentCoordN]
            if Direction.S in other.directions:
              r.append(other)
        case Direction.W:
          if self.adjacentCoordW is not None:
            other = map[self.adjacentCoordW]
            if Direction.E in other.directions:
              r.append(other)
        case Direction.E:
          if self.adjacentCoordE is not None:
            other = map[self.adjacentCoordE]
            if Direction.W in other.directions:
              r.append(other)
        case Direction.S:
          if self.adjacentCoordS is not None:
            other = map[self.adjacentCoordS]
            if Direction.N in other.directions:
              r.append(other)
    return r

class Ground(Tile): pass
class Start(Tile): 
  directions = [Direction.N, Direction.W, Direction.E, Direction.S]
  symbol = "S"
  distance = 0
class VerticalPipe(Tile): 
  directions = [Direction.N, Direction.S]
  symbol = "|"
class HorizontalPipe(Tile): 
  directions = [Direction.W, Direction.E]
  symbol = "-"
class BendL(Tile): 
  directions = [Direction.N, Direction.E]
  symbol = "L"
class BendJ(Tile): 
  directions = [Direction.N, Direction.W]
  symbol = "J"
class Bend7(Tile): 
  directions = [Direction.S, Direction.W]
  symbol = "7"
class BendF(Tile): 
  directions = [Direction.S, Direction.E]
  symbol = "F"

def getTile(coord: Coord, symbol: str) -> Tile:
  match symbol:
    case ".": 
      return Ground(coord)
    case "|": 
      return VerticalPipe(coord)
    case "-": 
      return HorizontalPipe(coord)
    case "L": 
      return BendL(coord)
    case "J": 
      return BendJ(coord)
    case "7": 
      return Bend7(coord)
    case "F": 
      return BendF(coord)
    case "S": 
      return Start(coord)

tileDict: dict[Coord, Tile] = dict()
startingTile: Tile = None
for y, line in enumerate(lines):
  s = ""
  for x, c in enumerate(line):
    coord = Coord(x, y)
    tile = getTile(coord, c)
    tileDict[coord] = tile
    if isinstance(tile, Start):
      startingTile = tile
    s += f"{tileDict[coord].symbol}"
  debug(s)
if startingTile is None:
  raise Exception("No starting tile found")

startingTile.isPartOfLoop = True

startingTileConnections: list[Tile] = startingTile.getConnectingTiles(tileDict)
debug(f"startingTile, {startingTile}, connections: {[str(c) for c in startingTileConnections]}")
if len(startingTileConnections) != 2:
  raise Exception(f"Unexpected number of starting tile connections, {len(startingTileConnections)}")

for tile in startingTileConnections:
  tile.distance = 1
  tile.isPartOfLoop = True

currentTileForwards = startingTileConnections[0]
currentTileForwards.distance = 1
currentTileBackwards = startingTileConnections[1]
currentTileBackwards.distance = 1
previousTileForwards = startingTile
previousTileBackwards = startingTile
distanceCount = 1
while True:
  distanceCount += 1

  connects = currentTileForwards.getConnectingTiles(tileDict)
  if len(connects) != 2:
    raise Exception(f"Unexpected number of tile connections, forward direction, {len(connects)} from {currentTileForwards}")
  isValidConnect = False
  for connect in connects:
    if connect.coord != previousTileForwards.coord:
      previousTileForwards = currentTileForwards
      currentTileForwards = connect
      isValidConnect = True
      currentTileForwards.isPartOfLoop = True
      break
  if not isValidConnect:
    raise Exception(f"Did not find a new tile for forward direction from {currentTileForwards}")

  connects = currentTileBackwards.getConnectingTiles(tileDict)
  if len(connects) != 2:
    raise Exception(f"Unexpected number of tile connections, backwards direction, {len(connects)} from {currentTileBackwards}")
  isValidConnect = False
  for connect in connects:
    if connect.coord != previousTileBackwards.coord:
      previousTileBackwards = currentTileBackwards
      currentTileBackwards = connect
      isValidConnect = True
      currentTileBackwards.isPartOfLoop = True
      break
  if not isValidConnect:
    raise Exception(f"Did not find a new tile for backwards direction from {currentTileBackwards}")
    
  if currentTileForwards.distance != None or \
      currentTileBackwards.distance != None:
    break

  currentTileForwards.distance = distanceCount
  currentTileBackwards.distance = distanceCount

# # # #
for y in range(0, nRows):
  s = ""
  for x in range(0, nColumns): 
    tile = tileDict[Coord(x, y)]
    if tile.distance is not None:
      # strInt = str(tile.distance)
      # s += f"{strInt[len(strInt) - 1]}"
      s += f"{tile.symbol}"
    else:
      # s += f"{tile.symbol}"
      s += f"."
  debug(s)
# # # #

# Get starting pipe replacement
startingPipeReplacement = None
startingPipeCoord = startingTile.coord
if startingTileConnections[0].coord.x == startingTile.coord.x:    # connect N/S
  if startingTileConnections[1].coord.x == startingTile.coord.x:    # other connect N/S
    startingPipeReplacement = VerticalPipe(startingPipeCoord)               # vertical
  elif startingTileConnections[0].coord.y < startingTile.coord.y:   # connect N
    if startingTileConnections[1].coord.x > startingTile.coord.x:     # other connect E
      startingPipeReplacement = BendL(startingPipeCoord)                     # L
    else:                                                             # other connect W
      startingPipeReplacement = BendJ(startingPipeCoord)                     # J
  elif startingTileConnections[0].coord.y > startingTile.coord.y:   # connect S
    if startingTileConnections[1].coord.x > startingTile.coord.x:     # other connect E
      startingPipeReplacement = BendL(startingPipeCoord)                     # F
    else:                                                             # other connect W
      startingPipeReplacement = BendJ(startingPipeCoord)                     # 7
elif startingTileConnections[0].coord.y == startingTile.coord.y:  # connect W/E
  if startingTileConnections[1].coord.y == startingTile.coord.y:    # other connect W/E
    startingPipeReplacement = HorizontalPipe(startingPipeCoord)            # horizontal
  elif startingTileConnections[0].coord.x < startingTile.coord.x:   # connect W
    if startingTileConnections[1].coord.y > startingTile.coord.y:     # other connect S
      startingPipeReplacement = Bend7(startingPipeCoord)                     # 7
    else:                                                             # other connect N
      startingPipeReplacement = BendJ(startingPipeCoord)                     # J
  elif startingTileConnections[0].coord.x > startingTile.coord.x:   # connect E
    if startingTileConnections[1].coord.y > startingTile.coord.y:     # other connect S
      startingPipeReplacement = BendF(startingPipeCoord)                     # F
    else:                                                             # other connect N
      startingPipeReplacement = BendL(startingPipeCoord)                     # L

debug(f"replacing starting pipe, {startingTile} with {startingPipeReplacement}")

startingPipeReplacement.isPartOfLoop = True
startingPipeReplacement.distance = 0
startingPipeReplacement.isInside = False
tileDict[startingTile.coord] = startingPipeReplacement

debug(f"{tileDict[startingTile.coord]}")

# # # #
for y in range(0, nRows):
  s = ""
  for x in range(0, nColumns): 
    tile = tileDict[Coord(x, y)]
    if tile.distance is not None:
      # strInt = str(tile.distance)
      # s += f"{strInt[len(strInt) - 1]}"
      s += f"{tile.symbol}"
    else:
      # s += f"{tile.symbol}"
      s += f"."
  debug(s)
# # # #

isInside = False
previousCorner = None
for y in range(nRows):
  isInside = False
  for x in range(nColumns):
    tile = tileDict[Coord(x, y)]
    # debug(f"scan {tile}")
    if tile.isPartOfLoop and isinstance(tile, VerticalPipe):
      isInside = not isInside
    elif tile.isPartOfLoop and (isinstance(tile, BendL) or isinstance(tile, BendF)):
      previousCorner = tile
    elif tile.isPartOfLoop and isinstance(tile, HorizontalPipe):
      pass
    elif tile.isPartOfLoop and (isinstance(tile, BendJ) or isinstance(tile, Bend7)):
      if previousCorner is not None:
        if isinstance(previousCorner, BendL) and isinstance(tile, BendJ) or \
            isinstance(previousCorner, BendF) and isinstance(tile, Bend7):
          pass # pipe turned back the direction it came
        else: # pipe crossed the line
          isInside = not isInside
        previousCorner = None
      else:
        raise Exception(f"encountered orphaned closing corner, {tile}")
    else:
      if isInside:
        tile.isInside = True

# # # #
debug(f"finished")
for y in range(0, nRows):
  s = ""
  for x in range(0, nColumns): 
    tile = tileDict[Coord(x, y)]
    if tile.distance is not None:
      # strInt = str(tile.distance)
      # s += f"{strInt[len(strInt) - 1]}"

      # s += f"{tile.symbol}"
      s += "*"
    elif tile.isInside:
      s += f"I"
    else:
      # s += f"{tile.symbol}"
      s += f"O"
  debug(s)
# # # #

insideCount = 0
for tile in tileDict.values():
  if tile.isInside:
    insideCount += 1

print(insideCount)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()