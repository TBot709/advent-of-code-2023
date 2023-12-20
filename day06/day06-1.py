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
# DEBUG = True
def debug(msg) -> None:
  if DEBUG:
    print(msg)
start = datetime.now()

# get input lines
puzzleNumber = "06"
# file = open(f"day{puzzleNumber}_example-input.txt",'r')
file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

times = lines[0].split()[1::]
debug(times)
distances = lines[1].split()[1::]
debug(distances)

class Race:
  def __init__(self, time: int, record: int):
    self.time = time
    self.record = record
  def __str__(self):
    return f"{self.time} {self.record}"
  def getNumWaysToBeatRecord(self) -> int:
    n = 0
    for x in range(0, self.time):
      timeRemaining = self.time - x
      distance = timeRemaining * x
      if distance > self.record:
        n += 1
    return n

races: list[Race] = []
for i, time in enumerate(times):
  races.append(Race(int(time), int(distances[i])))

product = 1
for race in races:
  numWays = race.getNumWaysToBeatRecord()
  debug(numWays)
  product *= numWays

print(product)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()