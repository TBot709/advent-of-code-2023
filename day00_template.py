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
file = open('day00_example-input.txt','r')
# file = open('day00_input.txt','r')
lines = file.readlines()
lines = list(map(lambda line: line.strip('\n'), lines))
nRows = len(lines)
nColumns = len(lines[0])
file.close()
debug(f"{nRows}, {nColumns}")
debug(f"{lines}")

print(0)

# # # # # # # # # # 

print('finished in ', end='')
print(datetime.now() - start, end='')
panic_thread.end()