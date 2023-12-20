#!/usr/bin/python

import sys
from datetime import datetime

DEBUG = True
# DEBUG = False
def debug(msg) -> None:
  if DEBUG:
    print(msg)
start = datetime.now()

# # # # # # # # # #
# file = open('day05_example-input.txt','r')
file = open('day05_input.txt','r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"{nRows}, {nColumns}")
debug(f"{lines}")

lineSeeds: str = lines[0]
seeds: list[int] = \
  list(
    map(
      lambda strSeed: int(strSeed.strip('\n ')), 
      lineSeeds.split(":")[1].split()))
debug(f"seeds: {seeds}")

class ValueMapper:
  def __init__(self, srcStart: int, destStart: int, range: int):
    self.srcStart = srcStart
    self.srcEnd = srcStart + range
    self.destStart = destStart
    self.destEnd = destStart + range
    self.range = range
  def __str__(self):
    return f"{self.destStart} {self.srcStart} {self.range}"
  def isInRange(self, value):
    return value >= self.srcStart and value < self.srcEnd
  def convert(self, value):
    diff = value - self.srcStart
    if (diff < 0):
      debug("CALLED CONVERT ON A VALUE LESS THAN START")
      return value
    return self.destStart + diff

def buildValueMapper(vmString):
  splitLine = vmString.split()
  return ValueMapper(
    int(splitLine[1]), 
    int(splitLine[0]), 
    int(splitLine[2]))

iLines = 0

seedToSoilMappers: list[ValueMapper] = []
debug("\nseed-to-soil-map:")
while lines[iLines] != "seed-to-soil map:":
  iLines += 1
iLines += 1
while lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  seedToSoilMappers.append(vm)
  iLines += 1

soilToFertilizerMappers: list[ValueMapper] = []
debug("\nsoil-to-fertilizer map:")
iLines += 2
while lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  soilToFertilizerMappers.append(vm)
  iLines += 1

fertilizerToWaterMappers: list[ValueMapper] = []
debug("\nfertilizer-to-water map:")
iLines += 2
while lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  fertilizerToWaterMappers.append(vm)
  iLines += 1

waterToLightMappers: list[ValueMapper] = []
debug("\nwater-to-light map:")
iLines += 2
while lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  waterToLightMappers.append(vm)
  iLines += 1

lightToTempMappers: list[ValueMapper] = []
debug("\nlight-to-temperature map:")
iLines += 2
while lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  lightToTempMappers.append(vm)
  iLines += 1

tempToHumidMappers: list[ValueMapper] = []
debug("\ntemperature-to-humidity map:")
iLines += 2
while lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  tempToHumidMappers.append(vm)
  iLines += 1

humidToLocationMappers: list[ValueMapper] = []
debug("\nhumidity-to-location map:")
iLines += 2
while iLines < nRows and lines[iLines] != "":
  vm = buildValueMapper(lines[iLines])
  debug(vm)
  humidToLocationMappers.append(vm)
  iLines += 1

listListMappers = [
  seedToSoilMappers,
  soilToFertilizerMappers,
  fertilizerToWaterMappers,
  waterToLightMappers,
  lightToTempMappers,
  tempToHumidMappers,
  humidToLocationMappers
]

values = seeds

for listMappers in listListMappers:
  debug(values)
  for i, value in enumerate(values): 
    for mapper in listMappers:
      if mapper.isInRange(value):
        values[i] = mapper.convert(value)
        break

debug(values)

lowestLocation = min(values)

print(lowestLocation)

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')