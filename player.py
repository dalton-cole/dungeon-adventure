#!/usr/bin/env python3

from random import random, randint
from print import slow_print, slow_input, set_options
from save import save_game
from numpy import full
from copy import deepcopy
from collections import defaultdict
from monsters import Monster
from dungeon import NormalRoom, MerchantRoom


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

allowable_actions = ['(f)ight', '(l)ook/ta(l)k', '(m)ove', '(o)pen', '(c)heck', '(u)se', '(s)ave', 'o(p)tions', '(q)uit']
action_shorthand_map = {
  'h' : 'help',
  'f' : 'fight',
  'l' : 'look',
  'm' : 'move',
  'o' : 'open',
  'c' : 'check',
  'u' : 'use',
  's' : 'save',
  'p' : 'options',
  'q' : 'quit'
}

allowable_classes = ['fighter', 'mage']
class_shorthand_map = {
  'f' : 'fighter',
  'm' : 'mage'
}

allowable_battle_actions = ['attack', 'item', 'run']
battle_action_shorthand_map = {
  'a' : 'attack',
  'i' : 'item',
  'r' : 'run'
}

allowable_movement_directions = ['north', 'south', 'east', 'west']
movement_shorthand_map = {
  'n' : 'north',
  's' : 'south',
  'e' : 'east',
  'w' : 'west'
}

def quit_game(*args):
  slow_print('See you next time!')
  exit()

def print_help(*args):
  slow_print('The following actions are available:')
  for action in allowable_actions:
    slow_print(f' - {action}')

class MovementError(Exception):
  def __init__(self, message):
    self.message = message
    super().__init__(self.message)
  def __str__(self):
    return f"{self.message}"

class Player:
  def __init__(self, start_location):
    self.gold = 0
    self.inventory = defaultdict(int)
    self.actions = {
      'help'    : print_help,
      'fight'   : self.battle,
      'look'    : self.look_around,
      'move'    : self.move,
      'open'    : self.open,
      'check'   : self.check,
      'use'     : self.use_item,
      'save'    : self.save_game,
      'options' : set_options,
      'quit'    : quit_game
    }
    self.battle_actions = {
      'attack' : self.attack_monster,
      'item'   : self.use_item,
      'run'    : self.run
    }
    while True:
      level = slow_input(f'Player starting level [{list(level_to_xp_map.keys())[0]} - {list(level_to_xp_map.keys())[-1]}]: ')
      try:
        level = int(level)
      except:
        slow_print(f'Level {level} is not allowed!')
        continue
      if level in level_to_xp_map:
        self.level = level
        break
      else:
        slow_print(f'Level {level} is not allowed!')
        continue
    self.player_class = slow_input('Player class [(f)ighter or (m)age]: ', shorthand_map=class_shorthand_map, allowable_inputs=allowable_classes)
    self.hp = level_to_hp_map[self.player_class][self.level]
    self.max_hp = level_to_hp_map[self.player_class][self.level]
    if self.player_class == 'fighter':
      self.accuracy = 0.9
      self.speed = 0.75
    elif self.player_class == 'mage':
      self.accuracy = 0.7
      self.speed = 0.5
    self.damage_lower, self.damage_upper = level_to_damage[self.player_class][self.level]
    self.experience_points = level_to_xp_map[self.level]
    self.location = start_location
    self.map = None

  def battle(self, labyrinth):
    if labyrinth.map[self.location].monsters:
      slow_print(f'You face {len(labyrinth.map[self.location].monsters)} monster(s)!')
      for monster in labyrinth.map[self.location].monsters:
        slow_print(f' - {monster.name}')
      while labyrinth.map[self.location].monsters:
        turn_order = sorted([self] + labyrinth.map[self.location].monsters, key=lambda x: x.speed)[::-1]
        for entity in turn_order:
          if entity.hp > 0:
            if isinstance(entity, Monster):
              entity.attack(self)
            else:
              if self.battle_actions[slow_input(f'What would you like to do? [(a)ttack, (i)tem, (r)un]: ', shorthand_map=battle_action_shorthand_map, allowable_inputs=allowable_battle_actions)](labyrinth, labyrinth.map[self.location].monsters) == 'escaped':
                self.check_level_up()
                return
      self.check_level_up()
    else:
      slow_print('There are no monsters to fight...')

  def action(self, labyrinth):
    if self.map is None:
      self.map = full(labyrinth.map.shape, '?')
    room = labyrinth.map[self.location]
    if isinstance(room, NormalRoom):
      if (not room.monsters) and (not room.treasure):
        self.map[self.location] = 'X'
      elif room.monsters:
        self.map[self.location] = 'D'
      elif room.treasure:
        self.map[self.location] = 'C'
    elif isinstance(room, MerchantRoom):
      self.map[self.location] = 'M'
    self.actions[slow_input(f'What would you like to do next? [(h)elp]: ', shorthand_map=action_shorthand_map, allowable_inputs=self.actions.keys())](labyrinth)

  def open(self, labyrinth):
    room = labyrinth.map[self.location]
    if not room.monsters:
      if room.treasure:
        slow_print(f'There are {len(room.treasure)} chest(s) in the room. You start opening...')
        while room.treasure:
          chest = room.treasure.pop(0)
          slow_print(f'You open a chest and find {chest.gold} gold!')
          if chest.item:
            slow_print(f'You also find {chest.item} inside!')
            self.inventory[chest.item] += 1
          self.gold += chest.gold
      else:
        slow_print('There are no chests in the room.')
    else:
      slow_print('You cannot open chests because the monsters are in the way!')

  def look_around(self, labyrinth):
    room = labyrinth.map[self.location]
    room.describe()
    if isinstance(room, MerchantRoom):
      choice = slow_input('Would you like to talk to the merchant? [y/n]', allowable_inputs=['y', 'n'])
      if choice == 'y':
        self.shop(room)

  def use_item(self, *args):
    if self.inventory:
      slow_print('Which item would you like to use? ')
      for i, (item, quantity) in enumerate(self.inventory.items()):
        slow_print(f' - [{i+1}] : {item} (Amount: {quantity})')
      idx = slow_input('', int, allowable_inputs=list(range(1, len(self.inventory)+1)))
      if list(self.inventory.keys())[idx-1] == 'health potion':
        if self.hp < self.max_hp:
          new_hp = min(self.max_hp, self.hp+8)
          slow_print(f'You heal {new_hp - self.hp} hp!')
          self.hp = new_hp
          slow_print(f'Current hp: {self.hp}')
          if self.inventory['health potion'] == 1:
            self.inventory.pop('health potion')
          else:
            self.inventory['health potion'] -= 1
        else:
          slow_print('Your hp is full!')
      else:
        slow_print('Item not available!')
    else:
      slow_print('Your bag is empty!')

  def move(self, labyrinth):
    room = labyrinth.map[self.location]
    if not room.monsters:
      try:
        self.change_room(labyrinth)
      except MovementError:
        slow_print("You can't go that way!")
        self.action(labyrinth)
    else:
      slow_print('You cannot move because the monsters block your path!')
      escape = slow_input('Would you like to attempt to escape? [y/n]', allowable_inputs=['y', 'n'])
      if escape == 'y':
        if self.escape_check(room.monsters):
          slow_print('You escaped!')
          self.change_room(labyrinth)
        else:
          slow_print('You could not escape!')
          self.battle(labyrinth)

  def change_room(self, labyrinth):
    slow_print('The following doors are available:')
    for door in labyrinth.map[self.location].doors:
      print(f'   - a door to the ({door[0]}){door[1:]}')
    loc = list(self.location)
    direction = slow_input("What direction do you go? ", shorthand_map=movement_shorthand_map, allowable_inputs=allowable_movement_directions)
    if direction == 'south':
      if self.location[0]+1 < labyrinth.map.shape[0]:
        loc[0] += 1
        slow_print(f'You head south and enter the next room...')
      else:
        raise MovementError("Cannot move south!")
    elif direction == 'west':
      if self.location[1] > 0:
        loc[1] -= 1
        slow_print(f'You head west and enter the next room...')
      else:
        raise MovementError("Cannot move west!")
    elif direction == 'east':
      if self.location[1]+1 < labyrinth.map.shape[1]:
        loc[1] += 1
        slow_print(f'You head east and enter the next room...')
      else:
        raise MovementError("Cannot move east!")
    elif direction == 'north':
      if self.location[0] > 0:
        loc[0] -= 1
        slow_print(f'You head north and enter the next room...')
      else:
        raise MovementError("Cannot move north!")
    self.location = tuple(loc)
    labyrinth.map[self.location].describe()

  def attack(self):
    if random() < self.accuracy:
      return randint(self.damage_lower, self.damage_upper)
    else:
      return 0

  def check(self, *args):
    slow_print(f'You have {self.gold} gold and {self.experience_points} experience (level {self.level})!')
    slow_print(f'Your current hit points are {self.hp}/{self.max_hp}.')
    if self.inventory:
      slow_print('You have the following items:')
      for item, quantity in self.inventory.items():
        slow_print(f'- {item} (Amount: {quantity})')
    if self.map is not None:
      slow_print('This is what your map looks like:')
      tmp_map = deepcopy(self.map)
      tmp_map[self.location] = '*'
      print('+---' * tmp_map.shape[1] + '+')
      for i in range(tmp_map.shape[0]):
        slow_print(f'| {" | ".join([c for c in tmp_map[i, :]])} |')
        print('+---' * tmp_map.shape[1] + '+')

  def shop(self, room: MerchantRoom):
    slow_print('You approach the merchant and inspect his wares...')
    slow_print('The following items are available:')
    for i, (item, price) in enumerate(room.items.items()):
      slow_print(f' - [{i+1}] : {item} ({price} g)')
    while True:
      choice = slow_input('Which would you like to buy? (# or (l)eave)', shorthand_map={'l' : 'leave'})
      if choice != 'leave':
        try:
          choice = int(choice)-1
        except:
          slow_print('Unrecognized command!')
          continue
        if 0 <= choice < len(room.items):
          if self.gold >= list(room.items.values())[choice]:
            slow_print(f'You purchase {list(room.items.keys())[choice]} for {list(room.items.values())[choice]} g...')
            self.inventory[list(room.items.keys())[choice]] += 1
            self.gold -= list(room.items.values())[choice]
            slow_print(f'Remaining gold: {self.gold}')
            continue
          else:
            slow_print("You don't have enough gold for that!")
            continue
        slow_print('That item is not available!')
      else:
        break
    print('The merchant nods and returns to his business.')

  def attack_monster(self, labyrinth, monsters):
    slow_print('Which monster do you attack? ')
    for i, monster in enumerate(monsters):
      if monster.hp > 0:
        slow_print(f' - [{i+1}] : {monster.name}')
    idx = slow_input('', int, allowable_inputs=list(range(1, len(monsters)+1)))
    damage = self.attack()
    if damage > 0:
      slow_print(f'You inflict {damage} damage on {monsters[idx-1].name}!')
      monsters[idx-1].hp = max(0, monsters[idx-1].hp - damage)
    else:
      slow_print('Oh no! You missed...')
    if monsters[idx-1].hp <= 0:
      slow_print(f'{monsters[idx-1].name} has died!')
      self.experience_points += monsters[idx-1].xp_worth
      monsters.pop(idx-1)

  def run(self, labyrinth, monsters):
    if self.escape_check(monsters):
      slow_print('You escaped!')
      self.change_room(labyrinth)
      return 'escaped'
    else:
      slow_print("You failed to escape!")

  def escape_check(self, monsters):
    avg_monster_accuracy = sum(monster.accuracy * monster.speed for monster in monsters) / len(monsters)
    return self.accuracy * self.speed > avg_monster_accuracy

  def check_level_up(self):
    if self.level < 5:
      if self.experience_points > level_to_xp_map[self.level+1]:
        self.damage_lower, self.damage_upper = level_to_damage[self.player_class]
        self.hp = level_to_hp_map[self.player_class]
        self.level += 1
        slow_print(f'You leveled up to level {self.level}!')

  def save_game(self, labyrinth):
    save_game(self, labyrinth)
