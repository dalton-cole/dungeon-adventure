#!/usr/bin/env python3

from time import sleep


options = {
  'text delay' : 0.015
}

def print_settings():
  slow_print('Current options:')
  slow_print(f'Character print delay: {options['text delay']:n} s')

def set_options():
  while True:
    slow_print('Which option would you like to change? [# or (d)one]')
    slow_print('You can change the following options:')
    for i, k in enumerate([options]):
      slow_print(f' - {k} ({i+1})')
    choice = slow_input('')
    choice = 'done' if choice == 'd' else choice
    if choice != 'done':
      try:
        choice = int(choice)-1
      except:
        slow_print('Unrecognized command!')
        continue
      if 0 <= choice < len(options):
        value = slow_input('What value would you like to set?')
        try:
          value = float(value)
        except:
          slow_print("You can't set that value!")
          continue
        if 0 < value < 0.1:
          options[list(options.keys())[choice]] = value
          slow_print(f'Option {list(options.keys())[choice]} has been set to {list(options.values())[choice]}!')
          continue
        else:
          slow_print("You can't set that value!")
          continue
      slow_print('That option is not available!')
    else:
      break
  print('Options have been saved.')

def set_options_from_dict(opt_dict):
  options.update(opt_dict)

def slow_print(msg):
  for i in range(len(msg)):
    print(msg[:i+1], end='\r' if i+1 < len(msg) else '\n')
    sleep(options['text delay'])

def slow_input(msg, fn=str):
  slow_print(msg)
  return fn(input('').lower().strip())
