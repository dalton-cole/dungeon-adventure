#!/usr/bin/env python3

from random import choices, randint, random
from print import slow_print
from monsters import available_monsters
from items import Elixir, SuperElixir, MegaElixir
from weapons import VegaBlade, CygnusHammer
from spells import Eclipse, Supernova


chest_sizes = {
  'small'  : 0.5,
  'medium' : 0.3,
  'large'  : 0.15,
  'huge'   : 0.05
}
chest_size_to_iron = {
  'small'  : 100,
  'medium' : 500,
  'large'  : 1000,
  'huge'   : 5000
}
chest_size_to_item_weights = {
  'small'  : [0.60, 0.33, 0.05, 0.02],
  'medium' : [0.50, 0.30, 0.15, 0.05],
  'large'  : [0.35, 0.20, 0.35, 0.10],
  'huge'   : [0.20, 0.10, 0.20, 0.50]
}
max_chests_per_room = 3
max_number_monsters_per_room = 2

class TreasureChest:
  def __init__(self):
    self.size = choices(list(chest_sizes.keys()), weights=list(chest_sizes.values()))[0]
    self.iron = chest_size_to_iron[self.size]
    self.item = choices([None, Elixir(), SuperElixir(), MegaElixir()], weights=chest_size_to_item_weights[self.size])[0]

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
      self.monsters.append(choices(list(available_monsters.keys()), weights=list(available_monsters.values()))[0]())
  def describe(self):
    slow_print(f'You are in a room with:')
    slow_print(f' - {len(self.doors)} doors')
    for door in self.doors:
      slow_print(f'   - a door to the ({door[0]}){door[1:]}')
    for chest in self.treasure:
      slow_print(f' - a {chest.size} chest')
    if self.monsters:
      slow_print(f' - {len(self.monsters):n} monsters')
    for monster in self.monsters:
      slow_print(f'   - {monster.name}')

class MerchantRoom(Room):
  def generate(self):
    self.items = [
      Elixir(),
      SuperElixir(),
      MegaElixir(),
      VegaBlade(),
      CygnusHammer(),
      Eclipse(),
      Supernova()
    ]
  def describe(self):
    slow_print('A figure in a dark robe is hunched in the corner.')
    slow_print('"Iron for wares..." is heard in a steely voice.')

class Map:
  def __init__(self, size, fill_value=None):
    self.size = size
    self.map = [[fill_value for _ in range(self.size)] for _ in range(self.size)]

  def get_location(self, location):
    return self.map[location[0]][location[1]]

  def set_location(self, location, value):
    self.map[location[0]][location[1]] = value

  def ravel(self):
    return [room for row in self.map for room in row]

class Labyrinth:
  def __init__(self, size):
    while True:
      self.size = size
      self.map = Map(self.size)
      for i in range(self.size):
        for j in range(self.size):
          doors = []
          if i > 0:
            doors.append('north')
          if i+1 < self.size:
            doors.append('south')
          if j > 0:
            doors.append('west')
          if j+1 < self.size:
            doors.append('east')
          if random() < 0.1:
            self.map.set_location((i, j), MerchantRoom(doors))
          else:
            self.map.set_location((i, j), NormalRoom(doors))
      if any([room.monsters for room in self.map.ravel()]) and any([isinstance(room, MerchantRoom) for room in self.map.ravel()]):
        break
    self.start_location = [randint(0, size-1), randint(0, size-1)]

  def get_room(self, location):
    return self.map.get_location(location)
