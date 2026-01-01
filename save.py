#!/usr/bin/env python3

from os import listdir, mkdir, remove
from os.path import dirname, exists, getmtime, join as pjoin
from datetime import datetime
from pickle import load, dump
from print import slow_input, slow_print, options


save_path = pjoin(dirname(__file__), '.saves')

def get_existing_save_files():
  if not exists(save_path):
    mkdir(save_path)
  return sorted([f.split('.')[0] for f in listdir(save_path) if f.endswith('.pkl')])

def print_existing_save_files():
  if get_existing_save_files():
    slow_print('The following files are present:')
  for save_file in get_existing_save_files():
    slow_print(f' - {save_file} ({datetime.fromtimestamp(getmtime(pjoin(save_path, save_file + ".pkl"))).strftime("%m/%d/%Y %H:%M:%S")})')

def save_game(player, labyrinth):
  while True:
    print_existing_save_files()
    slot = slow_input(
      'What save slot should the game be saved to? [# or (r)eturn]',
      shorthand_map={'r' : 'return'}
    )
    if slot == 'return':
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

def edit_save_data(*args):
  choice = slow_input('Would you like to delete save data? [y/n]', allowable_inputs=['y', 'n'])
  if choice == 'y':
    while get_existing_save_files():
      slow_print('Which file would you like to delete? [enter file # or (r)eturn]')
      print_existing_save_files()
      fyle = slow_input(
        '',
        shorthand_map={'r' : 'return'},
        allowable_inputs=[str(f) for f in get_existing_save_files()] + ['return']
      )
      if fyle != 'return':
        fyle_path = pjoin(save_path, f'{fyle}.pkl')
        if exists(fyle_path):
          remove(fyle_path)
          slow_print(f'File {fyle} deleted...')
      else:
        break
  else:
    slow_print('Save data not modified.')

def autosave(player, labyrinth):
  save_data([player, labyrinth, options], pjoin(save_path, 'autosave.pkl'))
