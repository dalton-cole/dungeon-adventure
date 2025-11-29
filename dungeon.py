#!/usr/bin/env python3

from random import choices, randint, random
from numpy import empty
from print import slow_print
from monsters import Goblin, DarkKnight, Dragon


chest_sizes = ['small', 'medium', 'large', 'huge']
chest_size_to_gold = {
  'small'  : 100,
  'medium' : 500,
  'large'  : 1000,
  'huge'   : 5000
}
max_chests_per_room = 3
max_number_monsters_per_room = 3

class TreasureChest:
  def __init__(self):
    self.gold = chest_size_to_gold[choices(chest_sizes, weights=[0.5, 0.3, 0.15, 0.05])[0]]
    self.item = 'health potion' if random() > 0.5 else None

class Room:
  def __init__(self, doors):
    self.monsters = []
    self.treasure = []
    self.doors = doors
    self.generate()
  def describe(self):
    slow_print(f'You are in a room with:')
    slow_print(f' - {len(self.doors)} doors')
    for door in self.doors:
      print(f'   - a door to the {door}')
    slow_print(f' - {len(self.treasure):n} chests')
    if self.monsters:
      slow_print(f' - {len(self.monsters):n} monsters')
    for monster in self.monsters:
      slow_print(f'   - {monster.name}')
  def generate(self):
    for i in range(randint(0, max_chests_per_room)):
      self.treasure.append(TreasureChest())
    for i in range(randint(0, max_number_monsters_per_room)):
      self.monsters.append(choices([Goblin(), DarkKnight(), Dragon()], weights=[0.5, 0.4, 0.1])[0])

class Labyrinth:
  def __init__(self, size):
    self.map = empty((size, size), dtype=Room)
    for i in range(self.map.shape[0]):
      for j in range(self.map.shape[1]):
        doors = []
        if i > 0:
          doors.append('north')
        if i+1 < self.map.shape[0]:
          doors.append('south')
        if j > 0:
          doors.append('west')
        if j+1 < self.map.shape[1]:
          doors.append('east')
        self.map[i,j] = Room(doors)
    self.start_location = [randint(0, size-1), randint(0, size-1)]
