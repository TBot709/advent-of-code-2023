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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-short.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

wildChar = '?'

def combinations(
    rowLength: int, 
    clues: list[int], 
    blankChar='.', 
    xChar='#') -> list[str]:
  def helper(n, clues):
    if not clues:
      return [blankChar * n]
    else:
      clue, *rest = clues
      return [blankChar * i + xChar * clue + (blankChar if rest else '') + tail
          for i in range(n - clue + 1)
          for tail in helper(n - i - clue - (1 if rest else 0), rest)]
  return helper(rowLength, clues)

debug(f"combos, length 9 with [1,2,3], {combinations(9, [1,2,3])}")

def wildcard_equals(sWithWilds: str, s2: str, wildChar='?') -> bool:
    if len(sWithWilds) != len(s2):
        return False
    return all(c1 == wildChar or c1 == c2 for c1, c2 in zip(sWithWilds, s2))

debug(f"does wh?t equal what? {wildcard_equals('wh?t', 'what')}")

count = 0

for line in lines:
  row, clueString = line.split()
  clues = list(map(lambda s: int(s), clueString.split(',')))
  combos = combinations(len(row), clues)
  combos = list(filter(lambda combo: wildcard_equals(row, combo), combos))
  debug(f"for {line}")
  debug(f"\t{row} {clues} {len(combos)} {combos}")
  count += len(combos)

print(count)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()