#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread

panic_thread = PanicThread(
  threading.current_thread(), 
  PanicThread.ONE_GIGABYTE, 
  PanicThread.TEN_SECONDS)
panic_thread.start()

DEBUG = False
# DEBUG = True
def debug(msg) -> None:
  if DEBUG:
    print(msg)
start = datetime.now()

# # # # # # # # # #
# file = open('./day05/day05_example-input.txt','r')
file = open('./day05/day05_input.txt','r')
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

class ValueRange:
  def __init__(self, start: int, range: int):
    self.start = start
    self.range = range
    self.end = start + range - 1
  def __str__(self):
    # return f"{self.start} {self.range}"
    return f"(s:{self.start},e:{self.end},r:{self.range})"
  def isRangeOverlaps(self, vm: ValueMapper):
    return vm.isInRange(self.start) or vm.isInRange(self.end)
  ''' ValueRange.convert
  converts self start value using given ValueMapper
  Returns newly created range if self range was split, 
  or None if no new range needed to be created
  '''
  def convert(self, vm: ValueMapper) -> 'ValueRange': 
    # if range inside mapping
    if vm.isInRange(self.start) and vm.isInRange(self.end):
      debug(f"\t{self}: range inside mapping for {vm}")
      self.start = vm.convert(self.start)
      self.end = vm.convert(self.end)
      debug(f"\t\tconverted to {self}")
      return None
    # if range starts in mapping, but ends outside
    if vm.isInRange(self.start) and not vm.isInRange(self.end):
      debug(f"\t{self}: range starts in mapping for {vm}")
      endDiff = self.end - vm.srcEnd
      self.start = vm.convert(self.start)
      self.range = self.range - endDiff
      self.end = self.start + self.range
      newRange = ValueRange(vm.srcEnd, endDiff)
      debug(f"\t\tconverted to {self} and created new range {newRange}")
      return newRange
    # if range starts outside mapping, but ends insides it
    if not vm.isInRange(self.start) and vm.isInRange(self.end):
      debug(f"\t{self}: range ends in mapping for {vm}")
      startDiff = vm.srcStart - self.start
      newRange = ValueRange(self.start, startDiff)
      self.end = vm.convert(self.end)
      self.start = vm.destStart
      self.range = self.end - self.start
      debug(f"\t\tconverted to {self} and created new range {newRange}")
      return newRange

listSeedRanges: list[ValueRange] = []
startValues = seeds[0::2]
debug(f"startValues {startValues}")
ranges = seeds[1::2]
debug(f"ranges {ranges}")
for i, startValue in enumerate(startValues):
  seedRange = ValueRange(startValue, ranges[i])
  listSeedRanges.append(seedRange)

def debugRanges(ranges: list[ValueRange]):
  if DEBUG:
    debug(list(map(lambda range: f"{range}", ranges)))

listValueRanges = listSeedRanges
for listMappers in listListMappers:
  debugRanges(listValueRanges)
  for valueRange in listValueRanges:
    for mapper in listMappers:
      if valueRange.isRangeOverlaps(mapper):
        newRange = valueRange.convert(mapper)
        if newRange is not None:
          listValueRanges.append(newRange)
        break

debugRanges(listValueRanges)

lowestLocation = min(list(map(lambda valueRange: valueRange.start, listValueRanges)))

print(lowestLocation)

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()