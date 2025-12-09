#!/usr/bin/env python3

from os import listdir, mkdir
from os.path import dirname, exists, join as pjoin
from pickle import load, dump
from print import slow_input, slow_print, options


save_path = pjoin(dirname(__file__), '.saves')

def get_existing_save_files():
  if not exists(save_path):
    mkdir(save_path)
  return [int(f.split('.')[0]) for f in listdir(save_path) if f.endswith('.pkl')]

def print_existing_save_files():
  slow_print('The following files are present:')
  for save_file in get_existing_save_files():
    slow_print(f' - {save_file}')

def save_game(player, labyrinth):
  while True:
    print_existing_save_files()
    slot = slow_input('What save slot should the game be saved to? [# or (c)ancel]', shorthand_map={'c' : 'cancel'})
    if slot == 'cancel':
      return
    try:
      slot = int(slot)
    except:
      slow_print('Cannot save to a non-numeric slot!')
      continue
    p = pjoin(save_path, f'{slot}.pkl')
    if exists(p):
      choice = slow_input(f'Save slot {slot} already exists! Would you like to overwrite? [y/n]')
      if choice == 'y':
        save_data([player, labyrinth, options], p)
        break
      else:
        slow_print('Game not saved...')
        return
    else:
      save_data([player, labyrinth, options], p)
      break
  slow_print(f'Game successfully saved to slot {slot}!')

def load_data(file_path):
  with open(file_path, 'rb') as f:
    return load(f)

def save_data(save_list, file_path):
  with open(file_path, 'wb') as f:
    dump(save_list, f)
