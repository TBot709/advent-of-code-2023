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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-1.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-2.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
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

startingTileConnections: list[Tile] = startingTile.getConnectingTiles(tileDict)
debug(f"startingTile, {startingTile}, connections: {[str(c) for c in startingTileConnections]}")
if len(startingTileConnections) != 2:
  raise Exception(f"Unexpected number of starting tile connections, {len(startingTileConnections)}")

for tile in startingTileConnections:
  tile.distance = 1

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
      break
  if not isValidConnect:
    raise Exception(f"Did not find a new tile for backwards direction from {currentTileBackwards}")
    
  if currentTileForwards.distance != None or \
      currentTileBackwards.distance != None:
    break

  currentTileForwards.distance = distanceCount
  currentTileBackwards.distance = distanceCount

# # # #
# s = "\n"
# for y in range(0, nRows):
#   for x in range(0, nColumns): 
#     tile = tileDict[Coord(x, y)]
#     if tile.distance is not None:
#       s += f"\td{tile.distance}\t"
#     else:
#       s += f"\t{tile.symbol}\t"
#   s += "\n"
# debug(s)
# # # #

print(distanceCount - 1)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()