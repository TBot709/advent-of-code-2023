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
puzzleNumber = "11"
# file = open(f"day{puzzleNumber}_example-input.txt",'r')
file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

rowsWithoutGalaxies = []
for y, line in enumerate(lines):
  hasGal = False
  for c in line:
    if c == '#':
      hasGal = True
      break
  if not hasGal:
    rowsWithoutGalaxies.append(y)      

debug(rowsWithoutGalaxies)

columnsWithoutGalaxaies = []
for x in range(nColumns):
  hasGal = False
  for y in range(nRows):
    if lines[y][x] == '#':
      hasGal = True
      break
  if not hasGal:
    columnsWithoutGalaxaies.append(x)

debug(columnsWithoutGalaxaies)

expansionSize = 1000000
# expansionSize = 10
# expansionSize = 100
expansionChar = '!'
expansionRow = "".ljust(nColumns, expansionChar)

def buildNewLine(oldLine: str) -> str:
  newLine = ""
  for x, c in enumerate(oldLine):
    if x in columnsWithoutGalaxaies:
      newLine += "!"
    else:
      newLine += c
  return newLine

newLines = []
for y, line in enumerate(lines):
  if y in rowsWithoutGalaxies:
    newLines.append(buildNewLine(expansionRow))
  else:
    newLines.append(buildNewLine(line))

# # # #
debug(" 012345678901234567890123456789")
for i, line in enumerate(newLines): 
  debug(f"{str(i)[len(str(i)) - 1]}{line}")
# # # #

from coord import Coord

galaxies: list[Coord] = []
for y, line in enumerate(newLines):
  for x, c in enumerate(line):
    if c == '#':
      galaxies.append(Coord(x, y))

def numExpansionsBetweenCoords(c1: Coord, c2: Coord) -> int:
  cL = c1 if c1.x < c2.x else c2
  cR = c1 if c1.x >= c2.x else c2
  numColumns = 0 if cL.x == cR.x else \
      len(list(filter(
          lambda i: i > cL.x and i < cR.x, columnsWithoutGalaxaies
      )))
  cU = c1 if c1.y < c2.y else c2
  cD = c1 if c1.y >= c2.y else c2
  numRows = 0 if cU.y == cD.y else \
      len(list(filter(
          lambda i: i > cU.y and i < cD.y, rowsWithoutGalaxies
      )))
  return numColumns + numRows

def getDistance(c1: Coord, c2: Coord) -> int:
  distanceWithoutExpansion = abs(c1.x - c2.x) + abs(c1.y - c2.y)
  expansions = numExpansionsBetweenCoords(c1, c2)
  return distanceWithoutExpansion - expansions + expansions*expansionSize

sumShortestPaths = 0
for i, g in enumerate(galaxies):
  for otherG in galaxies[i + 1::]:
    shortestPath = getDistance(g, otherG)
    # debug(f"shortest path length between {g} and {otherG} is {shortestPath}")
    sumShortestPaths += shortestPath

print(sumShortestPaths)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()