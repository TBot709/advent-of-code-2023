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
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

time = int(lines[0].split(":")[1].replace(' ',''))
debug(time)
distance = int(lines[1].split(":")[1].replace(' ',''))
debug(distance)

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

# print(Race(time, distance).getNumWaysToBeatRecord())

# answer from bruteforce is 43364472

'''
speed = t
distance = t*(T - t)
distance = Tt - t*t
0 = -t*t + Tt - d

(0 = a(x*x) + bx + c)
x = t
a = -1
b = T
c = -d
'''

import cmath
def solve_quadratic(a, b, c):
    # calculate the discriminant
    d = (b**2) - (4*a*c)
    # find two solutions
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)
    return sol1, sol2

a = -1
b = time
c = -1*(distance + 1)

sol1, sol2 = solve_quadratic(a, b, c)

debug(f"{sol1}, {sol2}, {(sol2 - sol1)}, {(sol1 - sol2)}")

import math
print(math.ceil((sol1 - sol2).real))

# answer from quadratic is 43364472

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()