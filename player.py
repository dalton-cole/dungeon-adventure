#!/usr/bin/env python3

from print import slow_print, slow_input
from monsters import Monster
from random import random, randint


allowable_classes = ['fighter', 'mage']
level_to_xp_map = {
  1: 0,
  2: 100,
  3: 1000,
  4: 10000,
  5: 100000
}
level_to_hp_map = {
  'fighter' : {
    1: 10,
    2: 15,
    3: 25,
    4: 40,
    5: 60
  },
  'mage' : {
    1: 6,
    2: 10,
    3: 16,
    4: 28,
    5: 38
  }
}
level_to_damage = {
  'fighter' : {
    1: (5, 9),
    2: (8, 12),
    3: (10, 16),
    4: (12, 20),
    5: (18, 26)
  },
  'mage' : {
    1: (10, 14),
    2: (12, 16),
    3: (15, 22),
    4: (18, 25),
    5: (22, 32)
  }
}

allowable_actions = ['(f)ight', '(l)ook', '(m)ove', '(o)pen', '(c)heck', '(u)se']
allowable_battle_actions = ['(a)ttack', '(i)tem', '(r)un']

def battle(player, labyrinth):
  slow_print(f'You face {len(labyrinth.map[tuple(player.location)].monsters)} monster(s)!')
  for i, monster in enumerate(labyrinth.map[tuple(player.location)].monsters):
    slow_print(f' - {monster.name} ({i+1})')
  while labyrinth.map[tuple(player.location)].monsters:
    turn_order = sorted([player] + labyrinth.map[tuple(player.location)].monsters, key=lambda x: x.speed)[::-1]
    for entity in turn_order:
      if entity.hp > 0:
        if isinstance(entity, Monster):
          entity.attack(player)
        else:
          if player.battle_action(labyrinth, labyrinth.map[tuple(player.location)].monsters) == 'escaped':
            return

class MovementError(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
  def __str__(self):
    return f"{self.message}"

class Player:
  def __init__(self, start_location):
    self.gold = 0
    self.inventory = []
    level = slow_input('Player starting level: ', int)
    if level in level_to_xp_map:
      self.level = level
    else:
      raise ValueError(f'Level {level} is not allowed!')
    player_class = slow_input('Player class (fighter or mage): ').lower()
    if player_class in allowable_classes:
      self.player_class = player_class
      self.hp = level_to_hp_map[self.player_class][self.level]
      self.max_hp = level_to_hp_map[self.player_class][self.level]
      if self.player_class == 'fighter':
        self.accuracy = 0.9
        self.speed = 0.75
      elif self.player_class == 'mage':
        self.accuracy = 0.7
        self.speed = 0.5
      self.damage_lower, self.damage_upper = level_to_damage[self.player_class][self.level]
    else:
      raise ValueError(f'Player class {player_class} not recognized!')
    self.experience_points = level_to_xp_map[self.level]
    self.location = start_location
  def action(self, labyrinth):
    room = labyrinth.map[tuple(self.location)]
    choice = slow_input(f'What would you like to do next? ({allowable_actions}): ').lower().strip()
    if (choice == 'fight') or (choice == 'f'):
      battle(self, labyrinth)
      self.check_level_up()
    elif (choice == 'look') or (choice == 'l'):
      room.describe()
    elif (choice == 'move') or (choice == 'm'):
      if not room.monsters:
        try:
          self.move(labyrinth)
        except MovementError:
          slow_print("You can't go that way!")
          self.action(labyrinth)
      else:
        slow_print('You cannot move because the monsters block your path!')
    elif (choice == 'open') or (choice == 'o'):
      self.open(room)
    elif (choice == 'check') or (choice == 'c'):
      self.check()
    elif (choice == 'use') or (choice == 'u'):
      self.use_item()
    else:
      slow_print(f'Unrecognized action {choice}! Please try again.')
      self.action(labyrinth)
  def open(self, room):
    if not room.monsters:
      if room.treasure:
        slow_print(f'There are {len(room.treasure)} chest(s) in the room. You start opening...')
        while room.treasure:
          chest = room.treasure.pop(0)
          slow_print(f'You open a chest and find {chest.gold} gold!')
          if chest.item:
            slow_print(f'You also find {chest.item} inside!')
            self.inventory.append(chest.item)
          self.gold += chest.gold
      else:
        slow_print('There are no chests in the room.')
    else:
      slow_print('You cannot open chests because the monsters are in the way!')
  def look_around(self, labyrinth):
    labyrinth.map[self.location].describe()
  def use_item(self):
    if self.inventory:
      slow_print('Which item would you like to use? ')
      for i, item in enumerate(self.inventory):
        slow_print(f' - {item} ({i+1})')
      idx = slow_input('', int)
      if self.inventory[idx-1] == 'health potion':
        if self.hp < self.max_hp:
          new_hp = min(self.max_hp, self.hp+8)
          slow_print(f'You heal {new_hp - self.hp} hp!')
          self.hp = new_hp
          self.inventory.pop(idx-1)
        else:
          slow_print('Your hp is full!')
      else:
        slow_print('Item not available!')
    else:
      slow_print('Your bag is empty!')
  def move(self, labyrinth):
    direction = slow_input("What direction do you go? ").lower().strip()
    if (direction == 'south') or (direction == 's'):
      if self.location[0]+1 < labyrinth.map.shape[0]:
        self.location[0] += 1
        slow_print(f'You head south and enter the next room...')
      else:
        raise MovementError("Cannot move south!")
    elif (direction == 'west') or (direction == 'w'):
      if self.location[1] > 0:
        self.location[1] -= 1
        slow_print(f'You head west and enter the next room...')
      else:
        raise MovementError("Cannot move west!")
    elif (direction == 'east') or (direction == 'e'):
      if self.location[1]+1 < labyrinth.map.shape[1]:
        self.location[1] += 1
        slow_print(f'You head east and enter the next room...')
      else:
        raise MovementError("Cannot move east!")
    elif (direction == 'north') or (direction == 'n'):
      if self.location[0] > 0:
        self.location[0] -= 1
        slow_print(f'You head north and enter the next room...')
      else:
        raise MovementError("Cannot move north!")
    else:
      raise MovementError(f"Direction {direction} is not recognized!")
    labyrinth.map[tuple(self.location)].describe()
  def attack(self):
    if random() < self.accuracy:
      return randint(self.damage_lower, self.damage_upper)
    else:
      return 0
  def check(self):
    slow_print(f'You have {self.gold} gold and {self.experience_points} experience (level {self.level})!')
    slow_print(f'Your current hit points are {self.hp}/{self.max_hp}.')
    if self.inventory:
      slow_print('You have the following items:')
      for item in self.inventory:
        slow_print(f'- {item}')
  def battle_action(self, labyrinth, monsters):
    battle_action = slow_input(f'What would you like to do? ({allowable_battle_actions}): ').lower().strip()
    if (battle_action == 'attack') or (battle_action == 'a'):
      slow_print('Which monster do you attack? ')
      for i, monster in enumerate(monsters):
        if monster.hp > 0:
          slow_print(f' - {monster.name} ({i+1})')
      idx = slow_input('', int)
      damage = self.attack()
      if damage > 0:
        slow_print(f'You inflict {damage} damage on {monsters[idx-1].name}!')
        monsters[idx-1].hp -= damage
      else:
        slow_print('Oh no! You missed...')
      if monsters[idx-1].hp < 0:
        slow_print(f'{monsters[idx-1].name} has died!')
        self.experience_points += monsters[idx-1].xp_worth
        monsters.pop(idx-1)
    elif (battle_action == 'item') or (battle_action == 'i'):
      self.use_item()
    elif (battle_action == 'run') or (battle_action == 'r'):
      avg_monster_accuracy = sum(monster.accuracy * monster.speed for monster in monsters) / len(monsters)
      if self.accuracy * self.speed > avg_monster_accuracy:
        slow_print('You escaped!')
        self.move(labyrinth)
        return 'escaped'
      else:
        slow_print("You failed to escape!")
        self.battle_action(labyrinth, monsters)
    else:
      slow_print('Unknown action!')
      self.battle_action(labyrinth, monsters)
  def check_level_up(self):
    if self.level < 5:
      if self.experience_points > level_to_xp_map[self.level+1]:
        self.damage_lower, self.damage_upper = level_to_damage[self.player_class]
        self.hp = level_to_hp_map[self.player_class]
        self.level += 1
        slow_print(f'You leveled up to level {self.level}!')
