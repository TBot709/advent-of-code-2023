#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
# setDebug(True)

puzzleNumber = "13"
partNumber = "1"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  # PanicThread.TEN_SECONDS)
  PanicThread.ONE_HOUR)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-example-input-2.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
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

from coord import Coord

patterns = []
pattern = []
for iLine, line in enumerate(lines):
  if line != "":
    pattern.append(line)
  if line == "" or iLine == len(lines) - 1:
    patterns.append(pattern)
    pattern = []
    continue

# debug(f"{patterns}")

def verticalLineBetween(pattern) -> ():
  width = len(pattern[0])
  height = len(pattern)
  columnsToLeft = 0
  columnsToRight = 0
  for iBetweenLines in range(1, width):
    # debug(f"\tvlbtwn {iBetweenLines}:")
    iDistance = 0
    mismatchCoordsCount = 0
    while iBetweenLines + iDistance < width and \
        iBetweenLines - iDistance > 0:
      # debug(f"\t\tdistance {iDistance}:")
      iRow = 0
      while iRow < height:
        # debug(f"\t\t\trow {iRow}: {pattern[iRow][iBetweenLines - 1 - iDistance]} {pattern[iRow][iBetweenLines + iDistance]}")
        if pattern[iRow][iBetweenLines - 1 - iDistance] != pattern[iRow][iBetweenLines + iDistance]:
          mismatchCoordsCount += 1
        iRow += 1
      if mismatchCoordsCount > 1:
        break
      iDistance += 1
    if mismatchCoordsCount == 1:
      columnsToLeft = iBetweenLines
      columnsToRight = width - iBetweenLines
      break
  return (columnsToLeft, columnsToRight)

def horizontalLineBetween(pattern) -> ():
  width = len(pattern[0])
  height = len(pattern)
  rowsAbove = 0
  rowsBelow = 0
  for iBetweenLines in range(1, height):
    # debug(f"\thlbtwn {iBetweenLines}:")
    iDistance = 0
    mismatchCoordsCount = 0
    while iBetweenLines + iDistance < height and \
        iBetweenLines - iDistance > 0:
      # debug(f"\t\tdistance {iDistance}:")
      iColumn = 0
      while iColumn < width:
        # debug(f"\t\t\trow {iColumn}: {pattern[iBetweenLines - 1 - iDistance][iColumn]} {pattern[iBetweenLines + iDistance][iColumn]}")
        if pattern[iBetweenLines - 1 - iDistance][iColumn] != pattern[iBetweenLines + iDistance][iColumn]:
          mismatchCoordsCount += 1
        iColumn += 1
      if mismatchCoordsCount > 1:
        break
      iDistance += 1
    if mismatchCoordsCount == 1:
      rowsAbove = iBetweenLines
      rowsBelow = height - iBetweenLines
      break
  return (rowsAbove, rowsBelow)

sum = 0

for pattern in patterns:

  sPattern = ""
  for line in pattern:
    sPattern += line + '\n'
  debug(f"\n\nPATTERN\n{sPattern}")
  
  vlbtwn = verticalLineBetween(pattern)
  if not any(x == 0 for x in vlbtwn):
    debug(f"vlbtwn reflection {vlbtwn}")
    sum += vlbtwn[0]
    continue
  hlbtwn = horizontalLineBetween(pattern)
  if not any(x == 0 for x in hlbtwn):
    debug(f"hlbtwn reflection {hlbtwn}")
    sum += 100*hlbtwn[0]
    continue

  debug("NO REFLECTIONS!")
  
print(sum)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()