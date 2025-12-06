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
max_number_monsters_per_room = 2

class TreasureChest:
  def __init__(self):
    self.gold = chest_size_to_gold[choices(chest_sizes, weights=[0.5, 0.3, 0.15, 0.05])[0]]
    self.item = 'health potion' if random() > 0.5 else None

class Room:
  def __init__(self, doors):
    self.doors = doors
    self.monsters = []
    self.treasure = []
    self.generate()

class NormalRoom(Room):
  def generate(self):
    for _ in range(randint(0, max_chests_per_room)):
      self.treasure.append(TreasureChest())
    for _ in range(randint(0, max_number_monsters_per_room)):
      self.monsters.append(choices([Goblin(), DarkKnight(), Dragon()], weights=[0.5, 0.4, 0.1])[0])
  def describe(self):
    slow_print(f'You are in a room with:')
    slow_print(f' - {len(self.doors)} doors')
    for door in self.doors:
      print(f'   - a door to the ({door[0]}){door[1:]}')
    slow_print(f' - {len(self.treasure):n} chests')
    if self.monsters:
      slow_print(f' - {len(self.monsters):n} monsters')
    for monster in self.monsters:
      slow_print(f'   - {monster.name}')

class MerchantRoom(Room):
  def generate(self):
    self.items = {
      'health potion' : 100
    }
  def describe(self):
    slow_print('A figure in a dark robe is hunched in the corner.')
    slow_print('"Gold for wares..." is heard in a steely voice.')

class Labyrinth:
  def __init__(self, size):
    while True:
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
          if random() < 0.1:
            self.map[i,j] = MerchantRoom(doors)
          else:
            self.map[i,j] = NormalRoom(doors)
      if any([room.monsters for room in self.map.ravel()]) and any([isinstance(room, MerchantRoom) for room in self.map.ravel()]):
        break
    self.start_location = (randint(0, size-1), randint(0, size-1))
