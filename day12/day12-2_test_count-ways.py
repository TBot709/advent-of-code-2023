#!/usr/bin/python

import sys
import threading
import inspect
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(True)

puzzleNumber = "00"
partNumber = "0"

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

from day12.count_ways import count_ways 

setDebug(False)
assert(count_ways([1],"???") == 3)
assert(count_ways([1,1],"???") == 1)
assert(count_ways([1,1,1],"?????") == 1)
assert(count_ways([1,1],"?????") == 6)
assert(count_ways([1,1,3],"???.###") == 1)
assert(count_ways([1,1,3],".??..??...?##.") == 4)
assert(count_ways([1,3,1,6],"?#?#?#?#?#?#?#?") == 1)
assert(count_ways([4,1,1],"????.#...#...") == 1)
assert(count_ways([1,6,5],"????.######..#####.") == 4)
assert(count_ways([3,2,1],"?###????????") == 10)
assert(count_ways([1,1,3,1,1,3,1,1,3,1,1,3,1,1,3],".??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.") == 16384)
assert(count_ways([3,2,1,3,2,1,3,2,1,3,2,1,3,2,1],"?###??????????###??????????###??????????###??????????###????????") == 506250)
setDebug(True)

# print(0)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
