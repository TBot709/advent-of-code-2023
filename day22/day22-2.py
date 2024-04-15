#!/usr/bin/python

import threading
# import resource
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)
debug("debug is on")

puzzleNumber = "22"
partNumber = "2"

# initialize panic thread
panic_thread = PanicThread(
  threading.current_thread(),
  PanicThread.ONE_GIGABYTE,
  PanicThread.TEN_SECONDS)
panic_thread.start()

# start now, include file open in running time
start = datetime.now()

# get input lines
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input-2.txt", 'r')
# file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt", 'r')
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
# debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # day{puzzleNumber}-{partNumber} # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

class Coord:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and \
                self.y == other.y and \
                self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.z < other.z or \
                (self.z == other.z and self.y < other.y) or \
                (self.z == other.z and self.y == other.y and self.x < other.x)

    def __str__(self):
        return f"{self.x},{self.y},{self.z}"


class Block:
    def __init__(self, start: Coord, end: Coord):
        self.start = start
        self.end = end

        self.bottom = None
        self.top = None
        if self.start.z < self.end.z:
            self.bottom = self.start
            self.top = self.end
        else:
            self.bottom = self.end
            self.top = self.start
        
        self.north = None
        self.south = None
        if self.start.y < self.end.y:
            self.north = self.start
            self.south = self.end
        else:
            self.north = self.end
            self.south = self.start

        self.west = None
        self.east = None
        if self.start.x < self.end.x:
            self.west = self.start
            self.east = self.end
        else:
            self.west = self.end
            self.east = self.start

        self.isOneCube = self.start == self.end
        self.isVertical = not self.isOneCube and self.start.z != self.end.z
        self.isNorthToSouth = not self.isOneCube and not self.isVertical and \
                self.start.y != self.end.y
        self.isEastToWest = not self.isOneCube and not self.isVertical and \
                not self.isNorthToSouth

        self.symbol = None

        self.cubes = []
        self._initCubes()

    def _initCubes(self):
        if self.isOneCube:
            self.cubes.append(self.start)
            return

        q = None

        offsetFn = None
        def up():
            q.z += 1
        def south():
            q.y += 1
        def east():
            q.x += 1

        end = None
        if self.isVertical:
            offsetFn = up
            q = self.bottom
            end = self.top
        elif self.isNorthToSouth:
            offsetFn = south
            q = self.north
            end = self.south
        elif self.isEastToWest:
            offsetFn = east
            q = self.west
            end = self.east
        else:
            raise Exception("self.without direction flag set")

        # copy
        q = Coord(q.x, q.y, q.z)
        
        # debug(f"q = {q}, end = {end}, {self.isVertical}, {self.isNorthToSouth}, {self.isEastToWest}")

        while not q == end:
            self.cubes.append(Coord(q.x, q.y, q.z))
            # debug(f"\t{q}: {self}")
            offsetFn()
        self.cubes.append(Coord(q.x, q.y, q.z))
        # debug(f"\t{q}: {self}, {self.bottom}")
    
    def __str__(self):
        sCubes = "["
        for cube in self.cubes:
            sCubes += f"{cube}, "
        sCubes += "]"
        sSymbol = ""
        if self.symbol is not None:
            sSymbol += f"  <- {self.symbol}"
        return f"{self.start}~{self.end}  <- {sSymbol},  {sCubes}"

    def __lt__(self, other):
        return self.bottom < other.bottom or \
                (self.bottom == other.bottom and self.north < other.north) or \
                (self.bottom == other.bottom and self.north == other.north and  
                        self.east < other.east)

    def setSymbol(self, symbol: str):
        self.symbol = symbol


blocks = []
maxX = 0
maxY = 0 

def strBlocks(blocks):
    s = ""
    for block in blocks:
        s += '\n' + str(block)
    return s

for line in lines:
    sLine = line.split('~')
    sB1 = list(map(lambda s: int(s), sLine[0].split(',')))
    sB2 = list(map(lambda s: int(s), sLine[1].split(',')))

    block = Block(
                Coord(sB1[0], sB1[1], sB1[2]),
                Coord(sB2[0], sB2[1], sB2[2]))
    
    if maxX < block.west.x:
        maxX = block.west.x
    if maxY < block.south.y:
        maxY = block.south.y
    
    blocks.append(block)

# debug(f"{maxX} {maxY}")

blocks.sort()

for i, block in enumerate(blocks):
    block.setSymbol(chr(b'A'[0] + i % 26))

# debug(strBlocks(blocks))

maxZ = blocks[-1].top.z
# debug(maxZ)

EMPTY = '.'

layers = [[[EMPTY for _ in range(maxX + 1)] for _ in range(maxY + 1)] for _ in range(maxZ + 1)]

# debug(f"layers list {len(layers)} {len(layers[0])} {len(layers[0][0])}")

for block in blocks:
    for cube in block.cubes:
        # debug(cube)
        layers[cube.z][cube.y][cube.x] = block.symbol

def strLayers():
    s = "\n"
    for layer in layers:
        for row in layer:
            for c in row:
                s += str(c)
            s += '\n'
        s += '\n'
    return s

debug(strLayers())


def isFloating(block):
    isFloating = True
    if block.isVertical:
        cube = block.cubes[0]
        # debug(f"{cube} {block.bottom}, {block.top}, {block.symbol}, {block}")
        if cube.z == 1 or layers[cube.z - 1][cube.y][cube.x] != EMPTY:
            isFloating = False
    else:
        for cube in block.cubes:
            if cube.z == 1 or layers[cube.z - 1][cube.y][cube.x] != EMPTY:
                isFloating = False
                break
    return isFloating


# let blocks fall
isAllLanded = False
while not isAllLanded:
    isAllLanded = True
    for block in blocks:
        if isFloating(block):
            isAllLanded = False
            for cube in block.cubes:
                layers[cube.z][cube.y][cube.x] = EMPTY
                layers[cube.z - 1][cube.y][cube.x] = block.symbol
                cube.z -= 1
            
debug(strLayers())


def isAllLandedIfBlockWasRemoved(block):
    isAllLanded = True
    for cube in block.cubes:
        layers[cube.z][cube.y][cube.x] = EMPTY
    for b in blocks:
        if b == block:
            continue
        if isFloating(b):
            isAllLanded = False
            break
    for cube in block.cubes:
        layers[cube.z][cube.y][cube.x] = block.symbol
    return isAllLanded


removableCount = 0
for block in blocks:
    if isAllLandedIfBlockWasRemoved(block):
        debug(f"removable: {block}")
        removableCount += 1

sumOfChainReactions = 0
for block in blocks:
    chainReactionCount = 0
    removedBlocks: [(Coord, str)] = []
    
    def removeCubeFromLayers(cube):
        layers[cube.z][cube.y][cube.x] = EMPTY
        removedBlocks.append((Coord(cube.x, cube.y, cube.z), block.symbol))

    # remove block in question
    for cube in block.cubes:
        removeCubeFromLayers(cube)

    for b in blocks:
        if b == block:
            continue
        if isFloating(b):
            chainReactionCount += 1
            for cube in b.cubes:
                removeCubeFromLayers(cube)

    # replace removed blocks
    for rb in removedBlocks:
        layers[rb[0].z][rb[0].y][rb[0].x] = rb[1]

    sumOfChainReactions += chainReactionCount

print(sumOfChainReactions)

# # # # # # PUZZLE SOLUTION END # # # # # # #

print(f"finished in {datetime.now() - start}")
# peakMemory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
# print(f"peak memory: {peakMemory}")
panic_thread.end()
