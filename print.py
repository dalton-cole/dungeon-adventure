#!/usr/bin/env python3

from time import sleep


options = {
  'text delay' : 0.015
}

option_ranges = {
  'text delay' : (0, 0.1)
}

option_check_functions = {
  'text delay' : lambda x: option_ranges['text delay'][0] <= x < option_ranges['text delay'][1]
}

def print_settings():
  slow_print('Current options:')
  slow_print(f'Character print delay: {options['text delay']:n} s')

def set_options(*args):
  print_settings()
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
        choice_key = list(options.keys())[choice]
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
        if option_check_functions[choice_key](value):
          options[choice_key] = value
          slow_print(f'Option {choice_key} has been set to {list(options.values())[choice]}!')
          continue
        else:
          slow_print(f"You can't set that value (range: {option_ranges[choice_key][0]} - {option_ranges[choice_key][1]})!")
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
