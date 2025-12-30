#!/usr/bin/env python3

from time import sleep


options = {
  'text delay' : 0.008,
  'autosave'   : False
}

option_units = {
  'text delay' : 's',
  'autosave'   : None
}

option_ranges = {
  'text delay' : (0, 0.1)
}

option_conversion_functions = {
  'text delay' : float,
  'autosave'   : lambda x: True if x == '1' else False
}

option_check_functions = {
  'text delay' : lambda x: option_ranges['text delay'][0] <= x < option_ranges['text delay'][1],
  'autosave'   : lambda x: isinstance(x, bool)
}

def print_settings():
  slow_print('Current options:')
  for k, v in options.items():
    slow_print(f' - {k} : {v} {option_units[k] if option_units[k] is not None else ""}')

def set_options(*args):
  print_settings()
  while True:
    slow_print('Which option would you like to change? [enter # of option to change or (d)one]')
    slow_print('You can change the following options:')
    for i, k in enumerate(options):
      slow_print(f' - [{i+1}] : {k}')
    choice = slow_input('', shorthand_map={'d' : 'done'})
    if choice != 'done':
      try:
        choice = int(choice)-1
        choice_key = list(options.keys())[choice]
      except:
        slow_print('Unrecognized command!')
        continue
      if 0 <= choice < len(options):
        value = slow_input('What value would you like to set?', fn=option_conversion_functions[choice_key])
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

def slow_input(msg, fn=str, shorthand_map={}, allowable_inputs=[]):
  while True:
    slow_print(msg)
    inp = fn(input('').lower().strip())
    if shorthand_map:
      inp = shorthand_map[inp] if inp in shorthand_map else inp
    if allowable_inputs:
      if inp not in allowable_inputs:
        slow_print(f'Input "{inp}" is not allowed! Try again...')
        continue
    break
  return inp
