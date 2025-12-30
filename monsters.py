#!/usr/bin/env python3

from print import slow_print
from random import randint, random


health_per_con_point = 3

class Monster:
  def __init__(self):
    self.hp = self.attributes['SIZ'] * health_per_con_point
    self.assign_max_hp()

  def get_attribute_modifier(self, attr):
    return self.attributes[attr] - 10

  def attack(self, player):
    if randint(1, 20) + self.get_attribute_modifier('LUM') >= player.get_AC():
      damage = self.roll_damage() + self.get_attribute_modifier('LUM')
      player.hp = max(0, player.hp - damage)
      slow_print(f'{self.name} does {damage} damage! HP : {player.hp}/{player.max_hp}!')
      if player.hp <= 0:
        slow_print('Your HP is depleted...Game Over!')
        exit()
    else:
      slow_print(f'{self.name} attacks and misses!')

  def roll_initiative(self):
    return randint(1, 20) + self.get_attribute_modifier('VEL')

  def roll_damage(self):
    return randint(1, self.max_damage) + self.get_attribute_modifier('LUM')

  def assign_max_hp(self):
    self.max_hp = self.attributes['SIZ'] * health_per_con_point

class WhiteDwarf(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 10,
      'SIZ' : 4,
      'VEL' : 10
    }
    super().__init__()
    self.AC = 8
    self.max_damage = 4
    self.name = "White Dwarf"
    self.xp_worth = 30
    self.iron = randint(1, 3) * 100

class GasGiant(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 12,
      'SIZ' : 6,
      'VEL' : 8
    }
    super().__init__()
    self.AC = 12
    self.max_damage = 6
    self.name = "Gas Giant"
    self.xp_worth = 100
    self.iron = randint(2, 5) * 100

class DarkMatter(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 14,
      'SIZ' : 8,
      'VEL' : 10
    }
    super().__init__()
    self.AC = 14
    self.max_damage = 8
    self.name = "Dark Matter"
    self.xp_worth = 500
    self.iron = randint(3, 7) * 100

class StellarWyrm(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 16,
      'SIZ' : 10,
      'VEL' : 8
    }
    super().__init__()
    self.AC = 16
    self.max_damage = 10
    self.name = "Stellar Wyrm"
    self.xp_worth = 1000
    self.iron = randint(5, 10) * 100

available_monsters = {
  WhiteDwarf  : 0.4,
  GasGiant    : 0.3,
  DarkMatter  : 0.2,
  StellarWyrm : 0.1
}
