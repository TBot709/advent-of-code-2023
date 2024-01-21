#!/usr/bin/python

import sys
import threading
from datetime import datetime
from panic_thread import PanicThread
from debug import debug, setDebug

setDebug(False)
setDebug(True)

puzzleNumber = "15"
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
file = open(f"./day{puzzleNumber}/day{puzzleNumber}_short-input.txt",'r')
#file = open(f"./day{puzzleNumber}/day{puzzleNumber}_example-input.txt",'r')
#file = open(f"./day{puzzleNumber}/day{puzzleNumber}_input.txt",'r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"rows: {nRows}, columns: {nColumns}")
# debug(f"{lines}")

print(f"# # # # # #  Running solution for day{puzzleNumber}-{partNumber}  # # # # # #")

# # # # # # PUZZLE SOLUTION START # # # # # #

steps = lines[0].split(",")

def sillyHash(s: str) -> int:
    r = 0
    for c in s:
        r += ord(c)
        r *= 17
        r %= 256
    return r

boxes = ["" for _ in range(256)]

def sBoxes(boxes) -> str:
    s = "\n"
    for i, box in enumerate(boxes):
        s += f"{i} {box}\n" if box != "" else ""
    return s

                    #+ label + ":" + focalLength + "," \
for step in steps:
    debug(f"{step} {'=' in step} {'-' in step}")
    if "=" in step:
        splitStep = step.split("=")
        label = "[" + splitStep[0] + "]"
        iBox = sillyHash(splitStep[0])
        sBox = boxes[iBox]
        focalLength = splitStep[1]
        iExistingIndex = sBox.find(label)
        if iExistingIndex != -1:
            iNextComma = sBox.find(",",iExistingIndex)
            sBox = ((sBox[0:iExistingIndex - 1]) if iExistingIndex > 0 else "") \
                    + ("," if iExistingIndex > 0 and iNextComma != -1 else "") \
                    + label + ":" + focalLength \
                    + ("," if iNextComma != -1 else "") \
                    + (sBox[iNextComma + 1::] if iNextComma != -1 else "")
        else:
            if len(sBox) > 0:
                sBox = sBox + ","  + label + ":" + focalLength
            else:
                sBox = label + ":" + focalLength
        boxes[iBox] = sBox
        debug(f"\tlabel:{label} fl:{focalLength} index:{iExistingIndex} iBox:{iBox} sBox:{sBox}")
    elif "-" in step:
        splitStep = step.split("-")
        label = "[" + splitStep[0] + "]"
        iBox = sillyHash(splitStep[0])
        sBox = boxes[iBox]
        iExistingIndex = sBox.find(label)
        debug(f"\tlabel:{label} index:{iExistingIndex} iBox:{iBox} sBox:{sBox}")
        if iExistingIndex != -1:
            iNextComma = sBox.find(",",iExistingIndex)
            sBox = ((sBox[0:iExistingIndex - 1]) if iExistingIndex > 0 else "") \
                    + ("," if iExistingIndex > 0 and iNextComma != -1 else "") \
                    + (sBox[iNextComma + 1::] if iNextComma != -1 else "")
            boxes[iBox] = sBox
    else:
        raise Exception(f"invalid step, {step}")
    debug(f"{sBoxes(boxes)}") 

debug(f"\n\n{sBoxes(boxes)}") 
                        
sumFocusingPower = 0
for iBox, box in enumerate(boxes):
    if len(box) > 0:
        for iLense, lense in enumerate(box.split(",")):
            debug(f"{iBox} {box} {iLense} {lense} {lense.split(':')}")
            fp = iBox + 1
            fp *= iLense + 1 
            fp *= int(lense.split(":")[1])
            sumFocusingPower += fp

print(sumFocusingPower)

# # # # # # PUZZLE SOLUTION END # # # # # # # 

print(f"finished in {datetime.now() - start}")
panic_thread.end()
