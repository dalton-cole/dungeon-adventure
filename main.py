#!/usr/bin/env python3

from print import slow_print, slow_input
from player import Player
from dungeon import Labyrinth


def game_loop(player, labyrinth):
  slow_print('You wake up in a dimly lit room.')
  labyrinth.map[tuple(labyrinth.start_location)].describe()
  while any(room.monsters for room in labyrinth.map.ravel()):
    player.action(labyrinth)
  slow_print('You defeated all monsters! A portal to home opens...you win!')

if __name__ == '__main__':
  the_labyrinth = Labyrinth(slow_input('What size of labyrinth would you like?', int))
  the_player = Player(the_labyrinth.start_location)
  game_loop(the_player, the_labyrinth)
