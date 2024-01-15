#!/usr/bin/python

import sys
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
file = open('./day01/day01_input.txt','r')
lines = file.readlines()
file.close()

digits = "0123456789"
def findDigit(s):
  for char in s:
    if char in digits:
      return char
  return None

sum = 0

for line in lines:
  line = line.rstrip('\n')
  reverse = line[::-1]
  #print(f"{line} {reverse} \n")

  firstDigit = findDigit(line)
  if (firstDigit is None):
    raise Exception("No digit in line " + line)

  lastDigit = findDigit(reverse)
  if (lastDigit is None):
    raise Exception("No digit in line " + reverse)

  x = int(firstDigit + lastDigit)
  sum += x

print(sum)  

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')