#!/usr/bin/env python3

from os.path import dirname, join as pjoin
from pickle import load, dump


save_path = pjoin(dirname(__file__), '.saves')

def load_data(file_path):
  with open(file_path, 'rb') as f:
    return load(f)

def save_data(player, labyrinth, file_path):
  with open(file_path, 'wb') as f:
    dump([player, labyrinth], f)
