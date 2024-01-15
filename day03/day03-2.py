#!/usr/bin/python

import sys
from datetime import datetime

DEBUG = False
# DEBUG = True
def debug(msg) -> None:
  if DEBUG:
    print(msg)

start = datetime.now()

# # # # # # # # # #

# open and parse input file
file = open('./day03/day03_input.txt','r')
# file = open('day03_example-input.txt','r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()

debug(f"input size {nRows} x {nColumns}")

class Coord:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
  def __eq__(self, other):
    if isinstance(other, Coord):
      return self.x == other.x and self.y == other.y
    return False
  def __ne__(self, other):
    return not self.__eq__(other)
  def __hash__(self):
    return hash((self.x, self.y))
  def __str__(self):
    return f"({self.x},{self.y})"

# +--> x
# |
# v y
def getAdjacentCoords(x: int, y: int) -> list[Coord]:
  coords = []
  # top
  coords.append(Coord(x, y - 1))
  coords.append(Coord(x - 1, y - 1))
  coords.append(Coord(x + 1, y - 1))
  # left
  coords.append(Coord(x - 1, y))
  # right
  coords.append(Coord(x + 1, y))
  # bottom
  coords.append(Coord(x, y + 1))
  coords.append(Coord(x - 1, y + 1))
  coords.append(Coord(x + 1, y + 1))
  def isInBounds(coord):
    return coord.x >= 0 and \
      coord.x < nColumns and \
      coord.y >= 0 and \
      coord.y < nRows
  coords = filter(lambda coord: isInBounds(coord), coords)
  return coords

gearSymbol = "*"
strCurrentNumber = ""
setCoordsSymbolSearch = set()
dictGearCoordsToNumbers = dict()

def checkAndHandleNumber() -> None:
  global strCurrentNumber, setCoordsSymbolSearch
  debug(f"testing if {strCurrentNumber} is gear number")
  isGearNumber = False
  for coord in setCoordsSymbolSearch:
    try:
      char = lines[coord.y][coord.x]
    except IndexError:
      debug(f"\tIndex Error at {coord.y}, {coord.x}")
      raise 
    debug(f"\tchecking char {char} at {coord.x}, {coord.y}")
    if char == gearSymbol:
      isGearNumber = True
      break
  if isGearNumber:
    debug(f"\t{strCurrentNumber} is gear number for gear at {coord}.")
    if (dictGearCoordsToNumbers.get(coord) == None):
      dictGearCoordsToNumbers[coord] = []
    dictGearCoordsToNumbers[coord].append(int(strCurrentNumber))

isParsingNumber = False
   
def reset() -> None:
  global isParsingNumber, strCurrentNumber, setCoordsSymbolSearch
  isParsingNumber = False
  strCurrentNumber = ""
  setCoordsSymbolSearch = set()

strDigits = "0123456789"
for iLine, line in enumerate(lines):
  for iChar, char in enumerate(line):
    if char in strDigits: 
      isParsingNumber = True
      strCurrentNumber += char
      adjacentCoords = getAdjacentCoords(iChar, iLine)
      for coord in adjacentCoords:
        setCoordsSymbolSearch.add(coord)
      if (iChar == nColumns - 1):
        checkAndHandleNumber()
        reset()
    else:
      # if just finished parsing
      if isParsingNumber:
        checkAndHandleNumber()
      reset()

sumOfGearRatios = 0

for coord, gearNumbers in dictGearCoordsToNumbers.items():
  debug(f"gear at {coord} has numbers {gearNumbers}.")
  if len(gearNumbers) == 2:
    product = 1
    for gearNumber in gearNumbers:
      product *= gearNumber
    debug(f"\tthis is a valid gear, adding product, {product}, to existing sum, {sumOfGearRatios})")
    sumOfGearRatios += product

print(sumOfGearRatios)

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')