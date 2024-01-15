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
  PanicThread.ONE_DAY)
panic_thread.start()

# debug print method
DEBUG = False
# DEBUG = True
def debug(msg) -> None:
  if DEBUG:
    lineno = str(inspect.stack()[1].lineno)
    label = "line    "
    labelWithLineno = label[0:len(label) - len(lineno)] + lineno
    print(f"{labelWithLineno}: {msg}")
start = datetime.now()

# get input lines
puzzleNumber = "08"
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-1.txt",'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-2.txt",'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
debug(f"{lines}")

# # # # # # PUZZLE SOLUTION START # # # # # #

directionsString = lines[0]
# startingNodeKey = lines[2][0:3:]
# endingNodeKey = lines[nRows - 1][0:3:]
startingNodeKey = 'AAA'
endingNodeKey = 'ZZZ'

debug(directionsString)
debug(startingNodeKey)
debug(endingNodeKey)

class Node:
  def __init__(self, key: str, left: str, right: str):
    self.key = key
    self.left = left
    self.right = right
  def __str__(self):
    return f"{self.key} = ({self.left}, {self.right})"

nodes: dict[str, Node] = {}
for line in lines[2::]:
  key = line[0:3:]
  left = line[7:10:]
  right = line[12:15:]
  nodes[key] = Node(key, left, right)
  debug(nodes[key])

numSteps = 0

def left(currentNodeKey: str, nodes: dict[str, Node]):
  debug(f"{currentNodeKey} L to {nodes[currentNodeKey].left}, {numSteps}")
  return nodes[currentNodeKey].left
def right(currentNodeKey: str, nodes: dict[str, Node]):
  debug(f"{currentNodeKey} R to {nodes[currentNodeKey].right}, {numSteps}")
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
currentNodeKey = startingNodeKey
while True:
  numSteps += 1
  # debug(f"{numSteps}")

  if (iDirections >= lengthDirections):
    iDirections = 0
  direction = directions[iDirections]
  iDirections += 1

  currentNodeKey = direction(currentNodeKey, nodes)
  
  if currentNodeKey == endingNodeKey:
    debug(f"{currentNodeKey} reached in {numSteps} steps")
    break;

print(numSteps)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()