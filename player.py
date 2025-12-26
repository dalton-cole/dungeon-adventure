#!/usr/bin/env python3

from random import randint
from print import slow_print, slow_input, set_options
from save import save_game
from numpy import full
from copy import deepcopy
from collections import defaultdict
from monsters import Monster
from dungeon import NormalRoom, MerchantRoom
from weapons import MeleeWeapon, StarShard
from spells import AttackSpell, SolarFlare
from items import Item


level_to_xp_map = {
  1: 0,
  2: 100,
  3: 300,
  4: 700,
  5: 1400
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
attribute_points_per_level = 4
health_per_con_point = 3

allowable_actions = ['(f)ight', '(l)ook/ta(l)k', '(m)ove', '(o)pen', '(c)heck', '(u)se', '(a)ssign', '(s)ave', 'o(p)tions', '(q)uit']
action_shorthand_map = {
  'h' : 'help',
  'f' : 'fight',
  'l' : 'look',
  'm' : 'move',
  'o' : 'open',
  'c' : 'check',
  'u' : 'use',
  'a' : 'assign',
  's' : 'save',
  'p' : 'options',
  'q' : 'quit'
}

allowable_battle_actions = ['attack', 'item', 'run']
battle_action_shorthand_map = {
  'a' : 'attack',
  'i' : 'item',
  'r' : 'run'
}

allowable_movement_directions = ['north', 'south', 'east', 'west', 'cancel']
movement_shorthand_map = {
  'n' : 'north',
  's' : 'south',
  'e' : 'east',
  'w' : 'west',
  'c' : 'cancel'
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

class PlayerInventory:
  def __init__(self):
    self.items = defaultdict(int)

  def add_item(self, item):
    self.items[item] += 1

  def remove_item(self, item):
    if self.items[item] == 1:
      self.items.pop(item)
    else:
      self.items[item] -= 1

  def get_item_by_enumeration(self, num):
    if 1 <= num <= len(self.items):
      return list(self.items.keys())[num-1]
    else:
      return None

  def print_item_enumeration_and_amount(self):
    for i, (item, quantity) in enumerate(self.items.items()):
      slow_print(f' - [{i+1}] : {item.name} (Amount: {quantity})')

  def print_item_enumeration_amount_and_price(self):
    for i, item in enumerate(self.items):
      slow_print(f' - [{i+1}] : {item.name} (Quantity: {self.items[item]}) ({item.price} g)')

class Player:
  def __init__(self, start_location):
    self.gold = 0
    self.inventory = PlayerInventory()
    self.weapons = set()
    self.spells = set()
    self.actions = {
      'help'    : print_help,
      'fight'   : self.battle,
      'look'    : self.look_around,
      'move'    : self.move,
      'open'    : self.open,
      'check'   : self.check,
      'use'     : self.use_item,
      'assign'  : self.assign_attribute_points,
      'save'    : self.save_game,
      'options' : set_options,
      'quit'    : quit_game
    }
    self.battle_actions = {
      'attack' : self.attack_action,
      'item'   : self.use_item,
      'run'    : self.run
    }
    self.attributes = {
      'STR' : 10,
      'INT' : 10,
      'CON' : 10,
      'DEX' : 10
    }
    self.level = slow_input(
      f'Player starting level [{list(level_to_xp_map.keys())[0]} - {list(level_to_xp_map.keys())[-1]}]:',
      int,
      allowable_inputs=list(range(list(level_to_xp_map.keys())[0], list(level_to_xp_map.keys())[-1]+1))
    )
    self.experience_points = level_to_xp_map[self.level]
    self.location = start_location
    self.map = None
    self.attribute_points = attribute_points_per_level * (self.level - 1)

  def battle(self, labyrinth):
    if labyrinth.map[tuple(self.location)].monsters:
      slow_print(f'You face {len(labyrinth.map[tuple(self.location)].monsters)} monster(s)!')
      for monster in labyrinth.map[tuple(self.location)].monsters:
        slow_print(f' - {monster.name} ({monster.hp}/{monster.max_hp} HP)')
      while labyrinth.map[tuple(self.location)].monsters:
        turn_order = sorted([self] + labyrinth.map[tuple(self.location)].monsters, key=lambda x: x.roll_initiative())[::-1]
        for entity in turn_order:
          if entity.hp > 0:
            if isinstance(entity, Monster):
              entity.attack(self)
            else:
              if self.battle_actions[
                slow_input(
                  f'What would you like to do? [(a)ttack, (i)tem, (r)un]:',
                  shorthand_map=battle_action_shorthand_map,
                  allowable_inputs=allowable_battle_actions
                )
              ](labyrinth, labyrinth.map[tuple(self.location)].monsters) == 'escaped':
                self.check_level_up()
                return
      self.check_level_up()
    else:
      slow_print('There are no monsters to fight...')

  def action(self, labyrinth):
    if self.map is None:
      self.map = full(labyrinth.map.shape, '?')
    room = labyrinth.map[tuple(self.location)]
    if isinstance(room, NormalRoom):
      if (not room.monsters) and (not room.treasure):
        self.map[tuple(self.location)] = 'X'
      elif room.monsters:
        self.map[tuple(self.location)] = 'D'
      elif room.treasure:
        self.map[tuple(self.location)] = 'C'
    elif isinstance(room, MerchantRoom):
      self.map[tuple(self.location)] = 'M'
    self.actions[
      slow_input(
        f'What would you like to do next? [(h)elp]: ',
        shorthand_map=action_shorthand_map,
        allowable_inputs=self.actions.keys()
      )
    ](labyrinth)

  def open(self, labyrinth):
    room = labyrinth.map[tuple(self.location)]
    if not room.monsters:
      if room.treasure:
        slow_print(f'There are {len(room.treasure)} chest(s) in the room. You start opening...')
        while room.treasure:
          chest = room.treasure.pop(0)
          slow_print(f'You open a chest and find {chest.gold} gold!')
          if chest.item:
            slow_print(f'You also find {chest.item.name} inside!')
            self.inventory.add_item(chest.item)
          self.gold += chest.gold
      else:
        slow_print('There are no chests in the room.')
    else:
      slow_print('You cannot open chests because the monsters are in the way!')

  def look_around(self, labyrinth):
    room = labyrinth.map[tuple(self.location)]
    room.describe()
    if isinstance(room, MerchantRoom):
      choice = slow_input('Would you like to talk to the merchant? [y/n]', allowable_inputs=['y', 'n'])
      if choice == 'y':
        self.shop(room)

  def use_item(self, *args):
    if self.inventory.items:
      slow_print('Which item would you like to use? ')
      self.inventory.print_item_enumeration_and_amount()
      idx = slow_input('', int, allowable_inputs=list(range(1, len(self.inventory.items)+1)))
      item = self.inventory.get_item_by_enumeration(idx)
      if isinstance(item, Item):
        if item.is_usable(self):
          item.use(self)
          if item.is_consumable:
            self.inventory.remove_item(item)
        else:
          slow_print(item.not_usable_message)
      else:
        slow_print('Item not available!')
    else:
      slow_print('Your bag is empty!')

  def move(self, labyrinth):
    room = labyrinth.map[tuple(self.location)]
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
    slow_print('The following doors are available [enter direction or (c)ancel]:')
    for door in labyrinth.map[tuple(self.location)].doors:
      slow_print(f'   - a door to the ({door[0]}){door[1:]}')
    loc = list(self.location)
    direction = slow_input(
      'What direction do you go?',
      shorthand_map=movement_shorthand_map,
      allowable_inputs=allowable_movement_directions
    )
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
    elif direction == 'cancel':
      slow_print('You do not move.')
      return
    self.location = tuple(loc)
    labyrinth.map[tuple(self.location)].describe()

  def get_attribute_modifier(self, attr):
    return self.attributes[attr] - 10

  def check(self, *args):
    slow_print(f'You have {self.gold} gold and {self.experience_points} experience (level {self.level})!')
    slow_print(f'Your current HP is {self.hp}/{self.max_hp}.')
    if self.inventory.items:
      slow_print('You have the following items:')
      self.inventory.print_item_enumeration_and_amount()
    if self.map is not None:
      slow_print('This is what your map looks like:')
      tmp_map = deepcopy(self.map)
      tmp_map[tuple(self.location)] = '*'
      slow_print('+---' * tmp_map.shape[1] + '+')
      for i in range(tmp_map.shape[0]):
        slow_print(f'| {" | ".join([c for c in tmp_map[i, :]])} |')
        slow_print('+---' * tmp_map.shape[1] + '+')
    slow_print('ATTRIBUTES')
    for attr, val in self.attributes.items():
      slow_print(f'{attr} : {val:>2d} ({self.get_attribute_modifier(attr):+d})')

  def assign_attribute_points(self, *args):
    if self.attribute_points > 0:
      while self.attribute_points > 0:
        choice = slow_input(
          'What attribute would you like to increase? [(s)tr, (i)nt, (c)on, (d)ex, (f)inish]',
          shorthand_map={'s' : 'str', 'i' : 'int', 'c' : 'con', 'd' : 'dex', 'f' : 'finish'},
          allowable_inputs=['str', 'int', 'con', 'dex', 'finish']
        )
        if choice == 'finish':
          break
        choice = choice.upper()
        amount = slow_input(
          f'How many points to you assign to {choice}? [1 - {self.attribute_points}]',
          int,
          allowable_inputs=list(range(1, self.attribute_points+1))
        )
        self.attributes[choice] += amount
        self.attribute_points -= amount
        if choice == 'CON':
          self.hp += amount * health_per_con_point
        slow_print(f'{choice} is increased to {self.attributes[choice]}. You have {self.attribute_points} points left.')
      self.assign_max_hp()
    else:
      slow_print('You do not have any points to assign!')

  def shop(self, room: MerchantRoom):
    slow_print('You approach the merchant...')
    while True:
      buy_or_sell = slow_input(
        'Would you like to do? [(b)uy/(s)ell/(l)eave]',
        shorthand_map={'b' : 'buy', 's' : 'sell', 'l' : 'leave'},
        allowable_inputs=['buy', 'sell', 'leave']
      )
      if buy_or_sell != 'leave':
        if buy_or_sell == 'buy':
          slow_print('The following items are available:')
          for i, item in enumerate(room.items):
            slow_print(f' - [{i+1}] : {item.name} ({item.price} g)')
          while True:
            choice = slow_input(
              'Which would you like to buy? [# or (r)eturn]',
              shorthand_map={'r' : 'return'},
              allowable_inputs=[str(i+1) for i in range(len(room.items))] + ['return']
            )
            if choice != 'return':
              try:
                choice = int(choice)-1
              except:
                slow_print('Unrecognized command!')
                continue
              item = room.items[choice]
              if isinstance(item, MeleeWeapon) and (not isinstance(self, Fighter)):
                slow_print('You cannot buy weapons...')
                continue
              if isinstance(item, AttackSpell):
                if not isinstance(self, Mage):
                  slow_print('You cannot buy spells...')
                  continue
                elif item in self.spells:
                  slow_print(f'You already know {item.name}!')
                  continue
                elif item in self.inventory.items:
                  slow_print(f'You have already purchased {item.name}!')
                  continue
              if 0 <= choice < len(room.items):
                if self.gold >= item.price:
                  slow_print(f'You purchase {item.name} for {item.price} g...')
                  self.inventory.add_item(item)
                  self.gold -= item.price
                  slow_print(f'Remaining gold: {self.gold}')
                  continue
                else:
                  slow_print("You don't have enough gold for that!")
                  continue
              slow_print('That item is not available!')
            else:
              break
        elif buy_or_sell == 'sell':
          if not self.inventory.items:
            slow_print("You don't have anything to sell!")
            continue
          while True:
            slow_print('What would you like to sell? [# or (r)eturn]')
            self.inventory.print_item_enumeration_amount_and_price()
            choice = slow_input(
              '',
              shorthand_map={'r' : 'return'},
              allowable_inputs=[str(i+1) for i in range(len(self.inventory.items))] + ['return']
            )
            if choice != 'return':
              try:
                choice = int(choice)
              except:
                slow_print('Unrecognized command!')
                continue
              if 1 <= choice <= len(self.inventory.items):
                item = self.inventory.get_item_by_enumeration(choice)
                if isinstance(item, MeleeWeapon) and isinstance(self, Fighter):
                  if sum(v if isinstance(k, MeleeWeapon) else 0 for k, v in self.inventory.items.items()) == 1:
                    slow_print("You can't sell your last weapon!")
                    continue
                slow_print(f'You sell {item.name} for {item.price} g...')
                self.gold += item.price
                self.inventory.remove_item(item)
                slow_print(f'Gold: {self.gold}')
              else:
                slow_print('That item is not available!')
                continue
            else:
              break
      else:
        break
    slow_print('The merchant nods and returns to his business.')
    self.weapons = set()
    for item in self.inventory.items:
      if isinstance(item, MeleeWeapon):
        if item not in self.weapons:
          self.weapons.add(item)
      elif isinstance(item, AttackSpell):
        if item not in self.spells:
          slow_print(f'You learn to cast {item.name}!')
          self.spells.add(item)
    if isinstance(self, Fighter):
      if self.equipped_weapon not in self.weapons:
        self.equipped_weapon = list(self.weapons)[0]
        slow_print(f'Your equipped weapon has been changed to {self.equipped_weapon.name}.')
    while any([isinstance(i, AttackSpell) for i in self.inventory.items]):
      for item in self.inventory.items:
        self.inventory.remove_item(item)
        break

  def run(self, labyrinth, monsters):
    if self.escape_check(monsters):
      slow_print('You escaped!')
      self.change_room(labyrinth)
      return 'escaped'
    else:
      slow_print("You failed to escape!")

  def escape_check(self, monsters):
    avg_monster_initiative = sum(monster.roll_initiative() for monster in monsters) / len(monsters)
    return self.roll_initiative() > avg_monster_initiative

  def check_level_up(self):
    if self.level < 5:
      if self.experience_points > level_to_xp_map[self.level+1]:
        self.damage_lower, self.damage_upper = level_to_damage[self.player_class]
        self.hp = level_to_hp_map[self.player_class]
        self.level += 1
        self.attribute_points += attribute_points_per_level
        slow_print(f'You leveled up to level {self.level}! You have {self.attribute_points} attribute points.')

  def save_game(self, labyrinth):
    save_game(self, labyrinth)

  def get_AC(self):
    return 10 + self.get_attribute_modifier('DEX')

  def roll_initiative(self):
    return randint(1, 20) + self.get_attribute_modifier('DEX')

  def assign_max_hp(self):
    self.max_hp = self.attributes['CON'] * health_per_con_point

class Fighter(Player):
  def __init__(self, start_location):
    super().__init__(start_location)
    self.attributes['STR'] += 2
    self.attributes['INT'] -= 2
    self.attributes['CON'] += 2
    self.attributes['DEX'] += 2
    self.hp = self.attributes['CON'] * health_per_con_point
    self.assign_max_hp()
    self.inventory.add_item(StarShard())
    self.weapons.add(StarShard())
    self.equipped_weapon = list(self.weapons)[0]

  def attack_action(self, labyrinth, monsters):
    slow_print('Which monster do you attack? ')
    for i, monster in enumerate(monsters):
      if monster.hp > 0:
        slow_print(f' - [{i+1}] : {monster.name} ({monster.hp}/{monster.max_hp} HP)')
    idx = slow_input('', int, allowable_inputs=list(range(1, len(monsters)+1)))
    self.attack(monsters[idx-1])
    if monsters[idx-1].hp <= 0:
      slow_print(f'{monsters[idx-1].name} has died!')
      self.experience_points += monsters[idx-1].xp_worth
      monsters.pop(idx-1)

  def attack(self, monster):
    if randint(1, 20) + self.get_attribute_modifier('STR') >= monster.AC:
      damage = self.equipped_weapon.roll_damage() + self.equipped_weapon.attack_bonus + self.get_attribute_modifier('STR')
      slow_print(f'You inflict {damage} damage on {monster.name}!')
      monster.hp = max(0, monster.hp - damage)
    else:
      slow_print('Oh no! You missed...')

  def check(self, *args):
    super().check()
    slow_print('You have the following weapons:')
    for weapon in self.weapons:
      slow_print(f' - {weapon.name}')
    slow_print(f'Your currently equipped weapon is {self.equipped_weapon.name}.')

class Mage(Player):
  def __init__(self, start_location):
    super().__init__(start_location)
    self.attributes['STR'] -= 2
    self.attributes['INT'] += 8
    self.attributes['CON'] -= 2
    self.hp = self.attributes['CON'] * health_per_con_point
    self.assign_max_hp()
    self.spells.add(SolarFlare())

  def attack_action(self, labyrinth, monsters):
    slow_print('What spell do you use?')
    for i, spell in enumerate(self.spells):
      slow_print(f' - [{i+1}] : {spell.name}')
    chosen_spell = list(self.spells)[slow_input('', int, allowable_inputs=list(range(1, len(self.spells)+1)))-1]
    if chosen_spell.range == 'single':
      slow_print('Which monster do you attack?')
      for i, monster in enumerate(monsters):
        if monster.hp > 0:
          slow_print(f' - [{i+1}] : {monster.name} ({monster.hp}/{monster.max_hp} HP)')
      idx = slow_input('', int, allowable_inputs=list(range(1, len(monsters)+1)))
      self.attack([monsters[idx-1]], chosen_spell)
    elif chosen_spell.range == 'multiple':
      self.attack(monsters, chosen_spell)
    while any([monster.hp <= 0 for monster in monsters]):
      for i, monster in enumerate(monsters):
        if monster.hp <= 0:
          slow_print(f'{monster.name} has died!')
          self.experience_points += monster.xp_worth
          monsters.pop(i)

  def attack(self, monsters, spell):
    damage = spell.roll_damage() + self.get_attribute_modifier('INT')
    for monster in monsters:
      if randint(1, 20) + self.get_attribute_modifier('INT') >= monster.AC:
        slow_print(f'You inflict {damage} damage on {monster.name}!')
        monster.hp = max(0, monster.hp - damage)
      else:
        slow_print(f'Oh no! You missed {monster.name}...')

  def check(self, *args):
    super().check()
    slow_print('You have the following spells:')
    for spell in self.spells:
      slow_print(f' - {spell.name}')
