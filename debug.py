#!/usr/bin/python

import inspect

DEBUG = False
def setDebug(isDebug: bool) -> None:
  global DEBUG
  DEBUG = isDebug

"""
  debug print method, with fixed-width line number labels
  be sure to setDebug(True) before the section you want to debug
"""
def debug(msg) -> None:
  if DEBUG:
    lineno = str(inspect.stack()[1].lineno)
    label = "line    "
    labelWithLineno = label[0:len(label) - len(lineno)] + lineno
    print(f"{labelWithLineno}: {msg}")