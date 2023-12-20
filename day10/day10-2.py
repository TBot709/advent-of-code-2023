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
  # PanicThread.TEN_SECONDS)
  PanicThread.ONE_HOUR)
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
  isOutside = False
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

startingTile.isPartOfLoop = True
startingTileConnections[0].isPartOfLoop = True
startingTileConnections[1].isPartOfLoop = True

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
    
  currentTileForwards.isPartOfLoop = True
  currentTileBackwards.isPartOfLoop = True
  
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

def getTile(c: Coord):
  if c is not None:
    return tileDict[c]
  return None

def getAdjacentTilesIfInBounds(c: Coord) -> list[Tile]:
  r = [
    getTile(getCoordIfInBounds(c.x, c.y - 1)), # Up
    getTile(getCoordIfInBounds(c.x + 1, c.y)), # Right
    getTile(getCoordIfInBounds(c.x, c.y + 1)), # Down
    getTile(getCoordIfInBounds(c.x - 1, c.y)), # Left
    getTile(getCoordIfInBounds(c.x - 1, c.y - 1)), # Diagonal Up-Left
    getTile(getCoordIfInBounds(c.x + 1, c.y - 1)), # Diagonal Up-Right
    getTile(getCoordIfInBounds(c.x + 1, c.y + 1)), # Diagonal Down-Right
    getTile(getCoordIfInBounds(c.x - 1, c.y + 1)), # Diagonal Down-Left
  ]
  return list(filter(lambda c: c is not None, r))

# Determine type of Starting pipe
startingPipeType = None
if startingTileConnections[0].coord.x == startingTile.coord.x:    # connect N/S
  if startingTileConnections[1].coord.x == startingTile.coord.x:    # other connect N/S
    startingPipeType = type(VerticalPipe(Coord(-1, -1)))              # vertical
  elif startingTileConnections[0].coord.y < startingTile.coord.y:   # connect N
    if startingTileConnections[1].coord.x > startingTile.coord.x:     # other connect E
      startingPipeType = type(BendL(Coord(-1, -1)))                     # L
    else:                                                             # other connect W
      startingPipeType = type(BendJ(Coord(-1, -1)))                     # J
  elif startingTileConnections[0].coord.y > startingTile.coord.y:   # connect S
    if startingTileConnections[1].coord.x > startingTile.coord.x:     # other connect E
      startingPipeType = type(BendL(Coord(-1, -1)))                     # F
    else:                                                             # other connect W
      startingPipeType = type(BendJ(Coord(-1, -1)))                     # 7
elif startingTileConnections[0].coord.y == startingTile.coord.y:  # connect W/E
  if startingTileConnections[1].coord.y == startingTile.coord.y:    # other connect W/E
    startingPipeType = type(HorizontalPipe(Coord(-1, -1)))            # horizontal
  elif startingTileConnections[0].coord.x < startingTile.coord.x:   # connect W
    if startingTileConnections[1].coord.y > startingTile.coord.y:     # other connect S
      startingPipeType = type(Bend7(Coord(-1, -1)))                     # 7
    else:                                                             # other connect N
      startingPipeType = type(BendJ(Coord(-1, -1)))                     # J
  elif startingTileConnections[0].coord.x > startingTile.coord.x:   # connect E
    if startingTileConnections[1].coord.y > startingTile.coord.y:     # other connect S
      startingPipeType = type(BendF(Coord(-1, -1)))                     # F
    else:                                                             # other connect N
      startingPipeType = type(BendL(Coord(-1, -1)))                     # L

if startingPipeType is None:
  raise Exception("Did not determine starting pipe type")
debug(f"startingPipeType {startingPipeType}")

def getOutsideEdgeTiles() -> list[Tile]:
  r = []
  for x in range(nColumns):
    r.append(tileDict[Coord(x,0)])
    r.append(tileDict[Coord(x,nRows - 1)])
  for y in range(nRows): 
    r.append(tileDict[Coord(0,y)])
    r.append(tileDict[Coord(nColumns - 1, y)])
  return list(filter(lambda t: not t.isPartOfLoop, r))

tileList = getOutsideEdgeTiles()
dummyHorizontalPipe = HorizontalPipe(Coord(-1, -1))
dummyVerticalPipe = VerticalPipe(Coord(-1, -1))
dummyBend7Pipe = Bend7(Coord(-1, -1))
dummyBendLPipe = BendL(Coord(-1, -1))
dummyBendJPipe = BendJ(Coord(-1, -1))
dummyBendFPipe = BendF(Coord(-1, -1))
for tile in tileList:
  # debug(f"\ttest for squeeze through {tile}")
  if tile.isPartOfLoop:
    continue
  tile.isOutside = True
  adjs = getAdjacentTilesIfInBounds(tile.coord)
  # adjs = filter(lambda t: not t.isOutside, adjs)
  for adj in adjs:
    # debug(f"\t\tchecking adjacent, {adj}, in loop? {adj.isPartOfLoop}, is known outside? {adj.isOutside}")
    if not adj.isPartOfLoop:
      if not adj.isOutside:
        adj.isOutside = True
        nextTiles = getAdjacentTilesIfInBounds(adj.coord)
        # nextTiles = list(filter(lambda t: not t.isOutside, nextTiles))
        tileList.extend(nextTiles)
    else:
      xNextDiff = 0
      yNextDiff = 0
      blockingPipeTypes = []
      if adj.coord.x == tile.coord.x and adj.coord.y > tile.coord.y: # down
        yNextDiff = 1
        blockingPipeTypes.append(type(dummyHorizontalPipe))
        if isinstance(adj, Bend7): 
          blockingPipeTypes.append(type(dummyBendLPipe))
        elif isinstance(adj, BendF): 
          blockingPipeTypes.append(type(dummyBendJPipe))
      if adj.coord.x == tile.coord.x and adj.coord.y < tile.coord.y: # up
        yNextDiff = -1
        blockingPipeTypes.append(type(dummyHorizontalPipe))
        if isinstance(adj, BendJ): 
          blockingPipeTypes.append(type(dummyBendFPipe))
        elif isinstance(adj, BendL): 
          blockingPipeTypes.append(type(dummyBend7Pipe))
      if adj.coord.x > tile.coord.x and adj.coord.y == tile.coord.y: # right
        xNextDiff = 1
        blockingPipeTypes.append(type(dummyVerticalPipe))
        if isinstance(adj, BendL): 
          blockingPipeTypes.append(type(dummyBend7Pipe))
        elif isinstance(adj, BendF): 
          blockingPipeTypes.append(type(dummyBendJPipe))
      if adj.coord.x < tile.coord.x and adj.coord.y == tile.coord.y: # left
        xNextDiff = -1
        blockingPipeTypes.append(type(dummyVerticalPipe))
        if isinstance(adj, Bend7): 
          blockingPipeTypes.append(type(dummyBendLPipe))
        elif isinstance(adj, BendJ): 
          blockingPipeTypes.append(type(dummyBendFPipe))

      # for diagonals, any loop pipe blocks
      if xNextDiff == 0 and yNextDiff == 0:
        if adj.isPartOfLoop:
          continue

      def isBlocking(tile: Tile, blockingPipeTypes) -> bool:
        isBlocking = \
          any(isinstance(tile, blockingPipeType) for blockingPipeType in blockingPipeTypes) or \
            (isinstance(tile, Start) and startingPipeType in blockingPipeTypes)  
        # if isBlocking:
          # debug("\t\t\t\t\tBLOCKED")
        return isBlocking

      if not isBlocking(adj, blockingPipeTypes):
        # debug(f"\t\t\tentering squeeze through loop for {adj}")
        tileSqueezeThrough = adj
        nextTileSqueezeThrough = None
        isValidTileSqueezeThrough = True
        while isValidTileSqueezeThrough:
          isValidTileSqueezeThrough = False
          nextCoord = getCoordIfInBounds(
            tileSqueezeThrough.coord.x + xNextDiff, 
            tileSqueezeThrough.coord.y + yNextDiff
          )
          # debug(f"\t\t\tsqueeze through tile, {tileSqueezeThrough}, nextCoord = {nextCoord}")
          if nextCoord is not None:
            nextTileSqueezeThrough = tileDict[nextCoord]
            # debug(f"\t\t\t\tnext squeeze through tile, {nextTileSqueezeThrough}")
            if nextTileSqueezeThrough.isPartOfLoop:
              if not isBlocking(nextTileSqueezeThrough, blockingPipeTypes):
                tileSqueezeThrough = nextTileSqueezeThrough
                isValidTileSqueezeThrough = True
            else:
              if not nextTileSqueezeThrough.isOutside:
                nextTileSqueezeThrough.isOutside = True
                nextTiles = getAdjacentTilesIfInBounds(nextTileSqueezeThrough.coord)
                # nextTiles = list(filter(lambda t: not t.isOutside, nextTiles))
                tileList.extend(nextTiles)
  # # # #
  # debug(f"for tile {tile}")
  # for y in range(0, nRows):
  #   s = ""
  #   for x in range(0, nColumns): 
  #     tile = tileDict[Coord(x, y)]
  #     if tile.distance is not None:
  #       # strInt = str(tile.distance)
  #       # s += f"{strInt[len(strInt) - 1]}"

  #       # s += f"{tile.symbol}"

  #       s += "*"
  #     elif tile.isOutside:
  #       s += f"O"
  #     else:
  #       s += f"{tile.symbol}"
  #       # s += f"I"
  #   debug(s)
  # # # #
                
# # # #
debug(f"finished")
for y in range(0, nRows):
  s = ""
  for x in range(0, nColumns): 
    tile = tileDict[Coord(x, y)]
    if tile.distance is not None:
      # strInt = str(tile.distance)
      # s += f"{strInt[len(strInt) - 1]}"

      s += f"{tile.symbol}"

      # s += "*"
    elif tile.isOutside:
      s += f"O"
    else:
      # s += f"{tile.symbol}"
      s += f"I"
  debug(s)
# # # #

insideCount = 0
for tile in tileDict.values():
  if not tile.isOutside and not tile.isPartOfLoop:
    insideCount += 1

print(insideCount)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()