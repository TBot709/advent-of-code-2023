#!/usr/bin/python

# my correct answer for part two: 4232520187524

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)

puzzleNumber = "12"
partNumber = "2"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  # PanicThread.TEN_SECONDS)
  PanicThread.ONE_DAY)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r') # answer was 21 for day12-1
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-short.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r') # answer was 8075 for day12-1
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # #  Running solution for day{puzzleNumber}-{partNumber}  # # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

# def wildcard_equals(sWithWilds: str, s2: str, wildChar='?') -> bool:
#     if len(sWithWilds) != len(s2):
#         return False
#     return all(c1 == wildChar or c1 == c2 for c1, c2 in zip(sWithWilds, s2))
# debug(f"does wh?t equal what? {wildcard_equals('wh?t', 'what')}")

def repeatWithSeparator(line: str, separator: str, numRepeats: int) -> str:
  return (line + separator) * (numRepeats - 1) + line 

# def numCombos(n, c): 
#   from math import comb
#   return comb(n, c)

sumOfProducts = 0

from day12.count_ways import count_ways 

isRepeating5Times = True

for i, line in enumerate(lines):
  row, clueString = line.split()

  if isRepeating5Times:
    row = repeatWithSeparator(row, "?", 5)
    clueString = repeatWithSeparator(clueString, ',', 5)

  clues = list(map(lambda s: int(s), clueString.split(',')))
  
  debug(f"{i} clues:{clues}, row:{row}")

  setDebug(False)
  count = count_ways(clues, row)
  setDebug(True)

  debug(f"count:{count}, sum:{sumOfProducts}")

  sumOfProducts += count

print(sumOfProducts)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
