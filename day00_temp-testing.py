#!/usr/bin/python

import sys
import threading
import inspect
from datetime import datetime
from panic_thread import PanicThread

puzzleNumber = "00"
partNumber = "0"

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
file = open(f"day{puzzleNumber}_example-input.txt",'r')
# file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # #  Running solution for day{puzzleNumber}-{partNumber}  # # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

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
    while windowEnd <= len(row) - spaceOfOtherClues:
      debug(f"\t     isFit?: {'| '*(level)}{row[windowStart:windowEnd:]} {clueString} {isFit(row[windowStart:windowEnd:], clueString)}")
      if isFit(row[windowStart:windowEnd:], clueString):
        # debug(f"\t           : {'| '*(level)}fit")
        nextLevel = level + 1
        nextClues = clues[1::]
        nextRow = row[windowEnd + 1::]
        if len(nextRow) > 0 and len(nextClues) > 0:
          _count_ways(nextClues, nextRow, nextLevel)
        else:
          if '#' in row[windowEnd + 1::]:
            debug(f"\t           : {'| '*(level)}invalid branch")
          else:
            if len(nextClues) == 0:
              debug(f"\t           : {'| '*(level)}valid branch")
              count += 1
      # else:
        # debug(f"\t           : {'| '*(level)}no fit")
      windowStart += 1
      windowEnd += 1
    debug(f"\t           : {'| '*(level)}end branch")
  _count_ways(clues, row)
  return count

DEBUG = False
assert(count_ways([1],"???") == 3)
assert(count_ways([1,1],"???") == 1)
assert(count_ways([1,1,1],"?????") == 1)
assert(count_ways([1,1],"?????") == 6)
assert(count_ways([1,1,3],"???.###") == 1)
DEBUG = True

# ???.### 1,1,3
# .??..??...?##. 1,1,3
print(count_ways([1,1,3],".??..??...?##."))

print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()