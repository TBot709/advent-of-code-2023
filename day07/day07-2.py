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
puzzleNumber = "07"
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-2.txt",'r')
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
from enum import Enum

HandType = Enum(
  'HandType', 
  [
    'HighCard',
    'OnePair',
    'TwoPair',
    'ThreeOfAKind',
    'FullHouse',
    'FourOfAKind',
    'FiveOfAKind'
  ]
)

CardType = Enum(
  'CardType',
  # ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
  ['J','2','3','4','5','6','7','8','9','T','Q','K','A'] # 'J', joker, lowest
)

def getHandType(s: str) -> HandType:
  # FiveOfAKind
  isFiveOfAKind = True
  for char in s[1::]:
    if char != s[0]:
      isFiveOfAKind = False
      break
  if isFiveOfAKind: 
    return HandType.FiveOfAKind
  #FourOfAKind
  for c1 in s[0:2:]:
    matches = 0
    for c2 in s:
      if c2 == c1:
        matches += 1
    if matches == 4:
      return HandType.FourOfAKind
  # FullHouse and ThreeOfAKind
  isThreeOfAKind = False
  for c1 in s[0:3:]:
    matches = 0
    for c2 in s:
      if c2 == c1:
        matches += 1
    if matches == 3:
      threeOfAKindChar = c1
      isThreeOfAKind = True
      break
  if isThreeOfAKind:
    otherChars = list(filter(lambda c: c != threeOfAKindChar, s))
    if otherChars[0] == otherChars[1]:
      return HandType.FullHouse
    else:
      return HandType.ThreeOfAKind
  # TwoPair and OnePair
  pair1Char = None
  for c1 in s:
    matches = 0
    for c2 in s:
      if c2 == c1:
        matches += 1
        if matches == 2:
          pair1Char = c1
          break
    if pair1Char is not None:
      break
  if pair1Char is not None:
    for c1 in s:
      matches = 0
      if c1 == pair1Char:
        continue
      for c2 in s:
        if c2 == c1:
          matches += 1
          if matches == 2:
            return HandType.TwoPair
    return HandType.OnePair
  # High Card
  return HandType.HighCard

def getStringWithReplacement(orig_string, index, char):
    return orig_string[:index] + char + orig_string[index+1:]

nonWildCardChars = "23456789TQKA"
def getBestHandType(hand: str):
  numJokers = hand.count('J')
  # if you have 5 or 4 wild cards, you will make 5 of a kind
  if numJokers == 5 or numJokers == 4:
    return HandType.FiveOfAKind
  if numJokers == 3:
    if getHandType(hand) == HandType.FullHouse:
      return HandType.FiveOfAKind
    else:
      return HandType.FourOfAKind
  if numJokers == 2:
    highestHandType = HandType.HighCard
    indiciesJokers = [i for i, c in enumerate(hand) if c == 'J']
    newHand = hand
    for nonWildC1 in nonWildCardChars:
      newHand = getStringWithReplacement(newHand, indiciesJokers[0], nonWildC1)
      for nonWildC2 in nonWildCardChars:
        newHand = getStringWithReplacement(newHand, indiciesJokers[1], nonWildC2)
        newHandType = getHandType(newHand)
        if newHandType.value > highestHandType.value:
          highestHandType = newHandType
    return highestHandType
  if numJokers == 1:
    highestHandType = HandType.HighCard
    indiciesJokers = [i for i, c in enumerate(hand) if c == 'J']
    newHand = hand
    for nonWildC1 in nonWildCardChars:
      newHand = getStringWithReplacement(newHand, indiciesJokers[0], nonWildC1)
      newHandType = getHandType(newHand)
      if newHandType.value > highestHandType.value:
          highestHandType = newHandType
    return highestHandType
  return getHandType(hand)

class Hand:
  def __init__(self, hand: str, bid: str):
    self.hand = hand
    self.bid = int(bid)
    self.handType: HandType = getBestHandType(hand)
    self.cardTypes: list[CardType] = list(map(lambda c: CardType[c], hand))
  def __str__(self):
    return f"{self.hand} {self.bid}\t{self.handType.name}"
  def __lt__(self, other):
    if isinstance(other, Hand):
      if self.handType.value == other.handType.value:
        # assess card value left to right
        for i, c in enumerate(self.cardTypes):
          otherCardType = other.cardTypes[i]
          if c.value == otherCardType.value:
            continue
          else:
            return c.value < otherCardType.value
        return False
      return self.handType.value < other.handType.value

hands: list[Hand] = []
for line in lines:
  splitLine = line.split()
  hand = Hand(splitLine[0], splitLine[1])
  debug(f"{hand}")
  hands.append(hand)

debug("\nsorting hands...\n")
hands.sort()

total = 0
rank = 0
for hand in hands:
  rank += 1
  score = hand.bid * rank
  total += score
  debug(f"rank {str(rank).zfill(2)}: {hand}\t\tscores {score}.\t\tTotal = {total}")

print(total)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()