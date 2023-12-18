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
puzzleNumber = "08"
# file = open(f"day{puzzleNumber}-2_example-input.txt",'r')
file = open(f"day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

directionsString = lines[0]
startingNodeKeySuffix = 'A'
endingNodeKeySuffix = 'Z'

debug(directionsString)

class Node:
  def __init__(self, key: str, left: str, right: str):
    self.key = key
    self.left = left
    self.right = right
  def __str__(self):
    return f"{self.key} = ({self.left}, {self.right})"

startingNodeKeys: list[str] = []
cycleCounters: list[int] = []
cycles: list[int] = []
lastZCount = []
nodes: dict[str, Node] = {}
for line in lines[2::]:
  key = line[0:3:]
  if key[2::] == startingNodeKeySuffix:
    debug(f"startingNode, {key}")
    startingNodeKeys.append(key)
    cycleCounters.append(0)
    cycles.append(0)
    lastZCount.append(0)
  left = line[7:10:]
  right = line[12:15:]
  nodes[key] = Node(key, left, right)
  # debug(nodes[key])

numSteps = 0

def left(currentNodeKey: str, nodes: dict[str, Node]):
  # debug(f"{currentNodeKey} L to {nodes[currentNodeKey].left}, {numSteps}")
  return nodes[currentNodeKey].left
def right(currentNodeKey: str, nodes: dict[str, Node]):
  # debug(f"{currentNodeKey} R to {nodes[currentNodeKey].right}, {numSteps}")
  return nodes[currentNodeKey].right

directions = []
for c in directionsString:
  if c == 'R':
    directions.append(right)
  elif c == 'L':
    directions.append(left)
  else:
    raise Exception(f"Unexpected direction, {c}")

iDirections = 0
lengthDirections = len(directions)
currentNodeKeys = startingNodeKeys
while True:
  numSteps += 1

  if (iDirections >= lengthDirections):
    iDirections = 0
  direction = directions[iDirections]
  iDirections += 1

  for i, key in enumerate(currentNodeKeys):
    currentNodeKeys[i] = direction(key, nodes)
  
  # debug(currentNodeKeys)
  isAllEndingNodes = True
  for i, key in enumerate(currentNodeKeys):
    cycleCounters[i] += 1
    if key[2] == endingNodeKeySuffix:
      if cycles[i] == 0:

        # consider first 'Z' from start as the cycle length
        # cycles[i] = cycleCounters[i]
        # cycleCounters[i] = 0

        # not counting the cycle length until it can be verified through two subsequent repeats
        if lastZCount[i] == 0:
          lastZCount[i] = cycleCounters[i]
        else:
          diff = cycleCounters[i] - lastZCount[i] 
          if diff == lastZCount[i]:
            cycles[i] = diff

      debug(f"\t{key} {key[2]} {endingNodeKeySuffix} {cycleCounters[i]} {lastZCount[i]} {cycles[i]}")
    else:
      isAllEndingNodes = False
  
  isAllCyclesDetermined = True
  for cycle in cycles:
    if cycle == 0:
      isAllCyclesDetermined = False
      break
  if isAllCyclesDetermined:
    from lcm import lcm_multiple
    lcm = lcm_multiple(cycles)
    debug(f"all cycles deteremined, {cycles}, lcm is {lcm}")
    numSteps = lcm
    break

  if isAllEndingNodes:
    break
    
print(numSteps)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()