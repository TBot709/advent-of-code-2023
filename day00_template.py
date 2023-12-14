#!/usr/bin/python

import sys
import threading
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
    print(msg)
start = datetime.now()

# get input lines
puzzleNumber = "00"
file = open(f"day{puzzleNumber}_example-input.txt",'r')
# file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()