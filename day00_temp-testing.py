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



print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()