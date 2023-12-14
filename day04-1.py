#!/usr/bin/python

import sys
from datetime import datetime

DEBUG = False
# DEBUG = True
def debug(msg) -> None:
  if DEBUG:
    print(msg)
start = datetime.now()

# # # # # # # # # #
# file = open('day04_example-input.txt','r')
file = open('day04_input.txt','r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"{nRows}, {nColumns}")
debug(f"{lines}")

def countToPoints(count: int) -> int:
  if count == 0:
    return 0
  points = 1
  for i in range(1, count):
    points *= 2
  return points

class Card:
  def __init__(self, nCard: int, winNums: list[int], playerNums: list[int]):
    self.nCard = nCard
    self.winNums = winNums
    self.playerNums = playerNums
  def __str__(self):
    return f"Card {self.nCard}: {winNums} | {playerNums}"
  def getNumMatches(self) -> int:
    count = 0
    for p in self.playerNums:
      if p in self.winNums:
        count += 1
    return count
  def getPoints(self) -> int:
    return countToPoints(self.getNumMatches())

points = 0
#dictCards: dict[Card] = dict()
for line in lines:
  cardNum = int(line.split(":")[0].split()[1])
  winNums = line.split(":")[1].split("|")[0].split()
  winNums = list(map(lambda num: int(num.strip()), winNums))
  playerNums = line.split(":")[1].split("|")[1].split()
  playerNums = list(map(lambda num: int(num.strip()), playerNums))
  card = Card(cardNum, winNums, playerNums)
  points += card.getPoints()
  debug(f"{line}\n{card}")
  debug(f"\t{card.getNumMatches()} matches, {card.getPoints()} points, running total {points}")
  #dictCards[cardNum] = Card(cardNum, winNums, playerNums)
  #debug(f"{line}\n{dictCards[cardNum]}")
  #debug(f"\t{dictCards[cardNum].getNumMatches()} matches, {dictCards[cardNum].getPoints()}")

print(points)

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')