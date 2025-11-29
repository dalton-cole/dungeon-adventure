#!/usr/bin/env python3

from print import slow_print
from player import Player
from dungeon import Labyrinth


if __name__ == '__main__':
  the_labyrinth = Labyrinth(2)
  the_player = Player(the_labyrinth.start_location)
  slow_print('You wake up in a dimly lit room.')
  the_labyrinth.map[tuple(the_labyrinth.start_location)].describe()
  while any(room.monsters for room in the_labyrinth.map.ravel()):
    the_player.action(the_labyrinth)
  slow_print('You defeated all monsters! A portal to home opens...you win!')
