#!/usr/bin/env python3

from os.path import exists, join as pjoin
from save import load_data, save_path, print_existing_save_files
from print import slow_print, slow_input, set_options_from_dict
from player import Player
from dungeon import Labyrinth


def game_loop(player, labyrinth):
  slow_print('You wake up in a dimly lit room.')
  labyrinth.map[tuple(labyrinth.start_location)].describe()
  while any(room.monsters for room in labyrinth.map.ravel()):
    player.action(labyrinth)
  slow_print('You defeated all monsters! A portal to home opens...you win!')

if __name__ == '__main__':
  while True:
    choice = slow_input('Would you like to start a (n)ew game or (l)oad a saved game?')
    if (choice == 'new game') or (choice == 'n'):
      the_labyrinth = Labyrinth(slow_input('What size of labyrinth would you like?', int))
      the_player = Player(the_labyrinth.start_location)
      break
    elif (choice == 'load') or (choice == 'l'):
      print_existing_save_files()
      slot = slow_input('Please enter the save slot number:', int)
      p = pjoin(save_path, f'{slot}.pkl')
      if exists(p):
        the_player, the_labyrinth, saved_options = load_data(p)
        set_options_from_dict(saved_options)
        break
      else:
        slow_print(f'Save slot {slot} does not exist!')
    else:
      slow_print('Unrecognized command!')

  game_loop(the_player, the_labyrinth)
