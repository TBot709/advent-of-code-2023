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
puzzleNumber = "12"
partNumber = "2"
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r') # answer was 21 for day12-1
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-short.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r') # answer was 8075 for day12-1
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # #  Running solution for day{puzzleNumber}-{partNumber}  # # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

def wildcard_equals(sWithWilds: str, s2: str, wildChar='?') -> bool:
    if len(sWithWilds) != len(s2):
        return False
    return all(c1 == wildChar or c1 == c2 for c1, c2 in zip(sWithWilds, s2))
#debug(f"does wh?t equal what? {wildcard_equals('wh?t', 'what')}")

def repeatWithSeparator(line: str, separator: str, numRepeats: int) -> str:
  return (line + separator) * (numRepeats - 1) + line 

def numCombos(n, c): 
  from math import comb
  return comb(n, c)

# def remainingSpaceNeeded(clues: list[int]) -> int:
#   r = 0
#   for clue in clues:
#     r += clue + 1
#   return r

def remainingSpaceNeeded(clues: list[int]) -> int:
  r = 0
  for clue in clues:
    r += clue
  return r

def isFit(s: str, clueString: str) -> bool:
  isFit = True
  for i, c in enumerate(s):
    clueC = clueString[i]
    if c == '?':
      continue
    if c == clueC:
      continue
    isFit = False
    break
  return isFit

def count_ways(clues: list[int], row: str) -> int:
  count = 0
  def _count_ways(clues: list[int], row: str, level=0):
    nonlocal count
    clue = clues[0]
    windowStart = 0
    windowEnd = clue
    clueString = '#'*clue
    spaceOfOtherClues = sum(clues[1::]) if len(clues) > 1 else 0
    debug(f"\t_count_ways: {'| '*(level)}{clues} {row} {spaceOfOtherClues}")
    while windowEnd < len(row) - spaceOfOtherClues:
      debug(f"\t      isFit: {'| '*(level)}{row[windowStart:windowEnd:]} {clueString} {isFit(row[windowStart:windowEnd:], clueString)}")
      if isFit(row[windowStart:windowEnd:], clueString):
        # debug(f"\t           : {'| '*(level)}fit")
        nextLevel = level + 1
        nextClues = clues[nextLevel::]
        nextRow = row[windowEnd + 1::]
        if len(nextRow) > 1 and len(nextClues) > 0:
          _count_ways(nextClues, nextRow, nextLevel)
        else:
          debug(f"{nextClues} {nextRow} {row[windowEnd + 1::]}")
          if '#' in row[windowEnd + 1::]:
            debug(f"\t           : {'| '*(level)}invalid branch")
            return
          else:
            debug(f"\t           : {'| '*(level)}valid branch")
            count += 1
            return
      # else:
        # debug(f"\t           : {'| '*(level)}no fit")
      windowStart += 1
      windowEnd += 1
    debug(f"\t           : {'| '*(level)}end branch")
  _count_ways(clues, row)
  return count

sumOfProducts = 0

for line in lines:
  row, clueString = line.split()
  # row = repeatWithSeparator(row, "?", 5)
  # clueString = repeatWithSeparator(clueString, ',', 5)
  clues = list(map(lambda s: int(s), clueString.split(',')))
  
  debug(f"clues:{clues}, row:{row}")

  count = count_ways(clues, row)

  debug(f"count:{count}, sum:{sumOfProducts}")

  sumOfProducts += count

# for line in lines:
#   row, clueString = line.split()

#   # row = repeatWithSeparator(row, "?", 5)

#   # clueString = repeatWithSeparator(clueString, ',', 5)
#   clues = list(map(lambda s: int(s), clueString.split(',')))
  
#   debug(f"{row} {clues}")

#   comboProduct = 1

#   rowCopy = "." + row + "."
#   rowCellCounts = [0]*len(rowCopy)
#   spaceTaken = 0
#   while len(rowCopy) > 0 and len(clues) > 0:
#     currentClue = clues[0]
#     clues = clues[1::]
#     currentRemainingSpaceNeeded = remainingSpaceNeeded(clues)
#     debug(f"\t{currentClue} {clues} {rowCopy} {currentRemainingSpaceNeeded} {spaceTaken}")

#     windowStart = spaceTaken
#     windowEnd = spaceTaken + currentClue + 2
#     sToFitIntoWindow = "." + ("#" * currentClue) + "."

#     nClueFits = 0
#     firstFitIndex = -1

#     while windowEnd - 1 <= len(rowCopy) - currentRemainingSpaceNeeded - 1:
#       window = rowCopy[windowStart:windowEnd:]
#       isClueFit = isFit(window, sToFitIntoWindow)
#       if (isClueFit):
#         nClueFits += 1
#         rowCellCounts[windowStart] += 1
#         if (firstFitIndex == -1):
#           firstFitIndex = windowStart

#       debug(f"\t\t{window} {sToFitIntoWindow} {isClueFit} {rowCellCounts}")
      
#       windowStart += 1
#       windowEnd += 1

#     if nClueFits == 0 or firstFitIndex == -1:
#       raise Exception(f"Found a clue with no fits, {currentClue} in {row} {clueString}")

#     #comboProduct *= numCombos(nClueFits, 1)
#     # debug(f"\t{comboProduct} {nClueFits} {numCombos(nClueFits, 1)}")

#     spaceTaken += len(sToFitIntoWindow) - 1

#   # reduce counts until there is only ones
#   # while any(x > 1 for x in rowCellCounts):
#   #   for i, x in enumerate(rowCellCounts):
#   #     if x > 1:
#   #       rowCellCounts[i] -= 1
#   # debug(f"\tafter reduction: {rowCellCounts}")

#   # multiple lengths of remaining segments
#   isInPlacement = False
#   placementCount = 0
#   for i, count in enumerate(rowCellCounts):
#     if count > 0:
#       placementCount += 1
#       isInPlacement = True
#     else:
#       isInPlacement = False
#     if not isInPlacement and placementCount > 0:
#       comboProduct *= placementCount
#       placementCount = 0

#   sumOfProducts += comboProduct
#   debug(f"\tcomboProduct: {comboProduct}, sumOfProducts: {sumOfProducts}")

#   # # # # 
#   # combos = combinations(len(row), clues)
#   # debug(f" {combos}")
#   # combos = list(filter(lambda combo: wildcard_equals(row, combo), combos))
#   # debug(f"for {line}")
#   # debug(f"\t{row} {clues} {len(combos)} {combos}")
#   # # # # 

#   # debug(f"2 choose 1 {numCombos(2, 1)}")
#   # debug(f"2 choose 1, 4 times {numCombos(2, 1)*numCombos(2, 1)*numCombos(2, 1)*numCombos(2, 1)}")

print(sumOfProducts)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()