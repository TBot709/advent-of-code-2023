#!/usr/bin/python

import sys
from datetime import datetime

DEBUG = False
# DEBUG = True
def debug(msg):
  if DEBUG:
    print(msg)

start = datetime.now()

# # # # # # # # # #

# open and parse input file
file = open('day03_input.txt','r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()

debug(f"input size {nRows} x {nColumns}")

class Coord:
  def __init__(self, x, y):
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

# +--> x
# |
# v y
def getAdjacentCoords(x, y):
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

strDigits = "0123456789"
nonPartSymbols = strDigits + "."
sumOfPartNumbers = 0
strCurrentNumber = ""
setCoordsSymbolSearch = set()

def checkAndHandleNumber():
  global sumOfPartNumbers, strCurrentNumber, setCoordsSymbolSearch
  debug(f"testing if {strCurrentNumber} is part number")
  isPartNumber = False
  for coord in setCoordsSymbolSearch:
    try:
      char = lines[coord.y][coord.x]
    except IndexError:
      debug(f"\tIndex Error at {coord.y}, {coord.x}")
      raise 
    debug(f"\tchecking char {char} at {coord.x}, {coord.y}")
    if char not in nonPartSymbols:
      isPartNumber = True
      break
  if isPartNumber:
    debug(f"\t{strCurrentNumber} is part number, adding to sumOfPartNumbers ({sumOfPartNumbers} += {strCurrentNumber}).")
    sumOfPartNumbers += int(strCurrentNumber)

isParsingNumber = False

def reset():
  global isParsingNumber, strCurrentNumber, setCoordsSymbolSearch
  isParsingNumber = False
  strCurrentNumber = ""
  setCoordsSymbolSearch = set()

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

print(sumOfPartNumbers)

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')