#!/usr/bin/env python3

from time import sleep


def slow_print(msg):
  for i in range(len(msg)):
    print(msg[:i+1], end='\r' if i+1 < len(msg) else '\n')
    sleep(0.015)

def slow_input(msg, fn=str):
  slow_print(msg)
  return fn(input('').lower().strip())
