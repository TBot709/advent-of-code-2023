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
puzzleNumber = "09"
# file = open(f"day{puzzleNumber}_example-input.txt",'r')
# file = open(f"day{puzzleNumber}_example-input-2.txt",'r')
file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

def getDifferences(numbers: list[int]) -> list[int]:
  length = len(numbers)
  r = []
  for i, n in enumerate(numbers):
    if i < length - 1:
      r.append(numbers[i + 1] - n)
  return r

def isAllZeros(numbers: list[int]) -> bool:
  for n in numbers:
    if n != 0:
      return False
  return True

def getNextNumber(numbers: list[int]) -> int:
  lists: list[list[int]] = [numbers]
  while not isAllZeros(lists[len(lists) - 1]):
    lists.append(getDifferences(lists[len(lists) - 1]))
  lastList = []
  for i, l in enumerate(lists[::-1]):
    if i == 0:
      l.append(0)
    else:
      l.append(l[-1] + lastList[-1])
    lastList = l
    # debug(f"\t{i}, {l}")
  return lists[0][-1]

sum = 0

for line in lines:
  numbers = list(map(lambda s: int(s), line.split()))
  nextNumber = getNextNumber(numbers)
  sum += nextNumber
  debug(f"nextNumber: {nextNumber}, for line {line}")

print(sum)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()