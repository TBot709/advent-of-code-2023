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
file = open('day02_input.txt','r')
lines = file.readlines()
file.close()

class Reveal:
  def __init__(self, r, g, b):
    self.r = r
    self.g = g
    self.b = b
  def __str__(self):
    sR, sG, sB = ["","",""]
    if self.r > 0: sR += f"{self.r} red"
    if self.g > 0: sG += f"{self.g} green"
    if self.b > 0: sB += f"{self.b} blue"
    return f"{sR}, {sG}, {sB}"

class Game:
  def __init__(self, n, reveals):
    self.n = n
    self.reveals = reveals
  def __str__(self):
    s = f"Game {self.n}: "
    for reveal in self.reveals:
      s += f"{reveal}; "
    return s

def buildRevealsFromString(strReveals):
  #print(f"strReveals {strReveals}")
  spltStrReveals = strReveals.split(';')
  #print(f"spltStrReveals {spltStrReveals}")
  reveals = []
  for reveal in spltStrReveals:
    #print(f"reveal.split(',') {reveal.split(',')}")
    spltReveal = reveal.split(',')
    r, g, b = [0, 0, 0]
    for countAndColor in spltReveal:
      countAndColor = countAndColor.strip(' ')
      countAndColor = countAndColor.strip('\n')
      #print(f"countAndColor.split(' ') {countAndColor.split(' ')}")
      x, color = countAndColor.split(' ')
      color = color.lower()
      if color == 'red':
        r = int(x)
      elif color == 'blue':
        b = int(x)
      elif color == 'green':
        g = int(x)
      else:
        raise Exception(f"Unrecognized color in {countAndColor}")
    reveals.append(Reveal(r,g,b))
  return reveals

gameDict = {}
for line in lines:
  line = line.strip('\n')
  #print(f"{line}")
  strGameLabel, strReveals = line.split(':')
  nGame = int(strGameLabel.split(' ')[1])
  reveals = buildRevealsFromString(strReveals)
  gameDict[nGame] = Game(nGame, reveals)
  #print(f"{gameDict[nGame]}")

def powerOfMinimumSetOfCubes(game):
  minR, minB, minG = [0,0,0]
  for reveal in game.reveals:
    if reveal.r > minR: minR = reveal.r
    if reveal.b > minB: minB = reveal.b
    if reveal.g > minG: minG = reveal.g
  return minR * minB * minG

sum = 0
for gameId, game in gameDict.items():
  sum += powerOfMinimumSetOfCubes(game)

print(f"{sum}")

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')