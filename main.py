#!/usr/bin/env python3

from os.path import exists, join as pjoin
from save import save_path, load_data, print_existing_save_files, get_existing_save_files, autosave
from print import slow_print, slow_input, set_options_from_dict, options
from player import Fighter, Mage
from dungeon import Labyrinth


allowable_classes = ['fighter', 'mage']
class_shorthand_map = {
  'f' : 'fighter',
  'm' : 'mage'
}
class_map = {
  'fighter' : Fighter,
  'mage'    : Mage
}

def game_loop(player, labyrinth):
  slow_print('You wake up in a dimly lit room.')
  slow_print('You sense a darkness that you must destroy...')
  labyrinth.get_room(player.location).describe(player)
  while any(room.monsters for room in labyrinth.map.ravel()):
    if options['autosave']:
      autosave(player, labyrinth)
    player.action(labyrinth)
  slow_print('You lit up the dark! A portal to home opens...you win!')

if __name__ == '__main__':
  while True:
    choice = slow_input(
      'Would you like to start a (n)ew game or (l)oad a saved game?',
      shorthand_map={'n' : 'new game', 'l' : 'load'},
      allowable_inputs=['new game', 'load']
    )
    if choice == 'new game':
      the_labyrinth = Labyrinth(
        slow_input(
          'What size of labyrinth would you like? [3 - 7]',
          int,
          allowable_inputs=list(range(3, 8))
        )
      )
      the_player = class_map[
        slow_input(
          'Player class [(f)ighter or (m)age]:',
          shorthand_map=class_shorthand_map,
          allowable_inputs=allowable_classes
        )
      ](the_labyrinth.start_location)
      break
    elif choice == 'load':
      if get_existing_save_files():
        print_existing_save_files()
        slot = slow_input(
          'Please enter the save slot to load:',
          allowable_inputs=get_existing_save_files()
        )
        p = pjoin(save_path, f'{slot}.pkl')
        if exists(p):
          the_player, the_labyrinth, saved_options = load_data(p)
          set_options_from_dict(saved_options)
          break
        else:
          slow_print(f'Save slot {slot} does not exist!')
      else:
        slow_print('No save files exist!')

  game_loop(the_player, the_labyrinth)
