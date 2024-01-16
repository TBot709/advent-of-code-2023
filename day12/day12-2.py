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
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r') # answer was 21 for day12-1
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-short.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r') # answer was 8075 for day12-1
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

def wildcard_equals(sWithWilds: str, s2: str, wildChar='?') -> bool:
    if len(sWithWilds) != len(s2):
        return False
    return all(c1 == wildChar or c1 == c2 for c1, c2 in zip(sWithWilds, s2))
debug(f"does wh?t equal what? {wildcard_equals('wh?t', 'what')}")

def repeatWithSeparator(line: str, separator: str, numRepeats: int) -> str:
  return (line + separator) * (numRepeats - 1) + line 

def numCombos(n, c): 
  from math import comb
  return comb(n, c)

def remainingSpaceNeeded(clues: list[int]) -> int:
  r = 0
  for clue in clues:
    r += clue + 1
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


count = 0

for line in lines:
  row, clueString = line.split()

  # row = repeatWithSeparator(row, "?", 5)

  # clueString = repeatWithSeparator(clueString, ',', 5)
  clues = list(map(lambda s: int(s), clueString.split(',')))
  
  debug(f"{row} {clues}")

  comboProduct = 1

  rowCopy = "." + row + "."
  while len(rowCopy) > 0 and len(clues) > 0:
    currentClue = clues[0]
    clues = clues[1::]
    currentRemainingSpaceNeeded = remainingSpaceNeeded(clues)
    debug(f"\t{rowCopy} {currentClue} {currentRemainingSpaceNeeded}")

    windowStart = 0
    windowEnd = currentClue + 2
    sToFitIntoWindow = "." + ("#" * currentClue) + "."

    while windowEnd < len(rowCopy) - 1:
      window = rowCopy[windowStart:windowEnd:]

      debug(f"\t\t{window} {sToFitIntoWindow} {isFit(window, sToFitIntoWindow)}")

      windowStart += 1
      windowEnd += 1

    # trim remaining
    rowCopy = rowCopy[(currentClue + 1)::]
    clues = clues[1::]

  # # # # 
  # combos = combinations(len(row), clues)
  # debug(f" {combos}")
  # combos = list(filter(lambda combo: wildcard_equals(row, combo), combos))
  # debug(f"for {line}")
  # debug(f"\t{row} {clues} {len(combos)} {combos}")
  # # # # 

  debug(f"2 choose 1 {numCombos(2, 1)}")
  debug(f"2 choose 1, 4 times {numCombos(2, 1)*numCombos(2, 1)*numCombos(2, 1)*numCombos(2, 1)}")

  


print(count)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()