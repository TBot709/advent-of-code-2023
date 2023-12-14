#!/usr/bin/python

import sys
import re
from datetime import datetime

DEFAULT_LIMIT = 1000

limit = 0

if len(sys.argv) > 1:
  for arg in sys.argv:
    limit = int(sys.argv[1])
else:
    limit = DEFAULT_LIMIT

start = datetime.now()

# # # # # # # # # #

# open and parse input file
file = open('day01_input.txt','r')
#file = open('day01-2_test-input.txt','r')
#file = open('day01-2_test-input-2.txt','r')
lines = file.readlines()
file.close()

digits = "123456789"
def findFirstIndexAndDigit(s):
  index = sys.maxsize
  digit = None
  for i, char in enumerate(s):
    if char in digits:
      if i < index:
        index = i
        digit = int(char)
  return [index, digit]
def findLastIndexAndDigit(s):
  index = -1
  digit = None
  for i, char in enumerate(s):
    if char in digits:
      if i > index:
        index = i
        digit = int(char)
  return [index, digit]

textNumbers = {
  1: "one",
  2: "two",
  3: "three",
  4: "four",
  5: "five",
  6: "six",
  7: "seven",
  8: "eight",
  9: "nine"
}
def findFirstTextNumberIndexAndDigit(s):
  index = sys.maxsize
  digit = None
  for d, text in textNumbers.items():
    matches = re.finditer(text, s)
    for match in matches:
      i = match.start()
      if i >= 0:
        if i < index: 
          index = i
          digit = d
  return [index, digit]
def findLastTextNumberIndexAndDigit(s):
  index = -1
  digit = None
  for d, text in textNumbers.items():
    matches = re.finditer(text, s)
    for match in matches:
      i = match.start()
      if i >= 0:
        if i > index: 
          index = i
          digit = d
  return [index, digit]

nLine = 0
sum = 0

for line in lines:
  nLine += 1
  line = line.rstrip('\n')
  line = line.lower()
  #print(f"{line}")

  firstIandD = findFirstIndexAndDigit(line)
  firstTextIandD = findFirstTextNumberIndexAndDigit(line)
  #print(f"first: {firstIandD} {firstTextIandD}")
  if (firstIandD[1] is None and firstTextIandD[1] is None):
    raise Error(f"No digits found in {line}")
  else:
    if (firstIandD[1] is None or firstIandD[0] > firstTextIandD[0]):
      firstDigit = firstTextIandD[1]
    else:
      firstDigit = firstIandD[1]

  lastIandD = findLastIndexAndDigit(line)
  lastTextIandD = findLastTextNumberIndexAndDigit(line)
  print(f"last: {lastIandD} {lastTextIandD}")
  if (lastIandD[1] is None or lastIandD[0] < lastTextIandD[0]):
    lastDigit = lastTextIandD[1]
  else:
    lastDigit = lastIandD[1]

  x = int(str(firstDigit) + str(lastDigit))
  print(f"{nLine}: {line} {firstDigit} {lastDigit} {x}")
  sum += x

print(sum)  

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')