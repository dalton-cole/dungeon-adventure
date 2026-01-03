#!/usr/bin/env python3

from print import slow_print
from random import randint
from math import floor


health_per_con_point = 2

class Monster:
  def __init__(self):
    self.hp = self.attributes['SIZ'] * health_per_con_point
    self.assign_max_hp()

  def get_attribute_modifier(self, attr):
    return floor((self.attributes[attr] - 10) / 2)

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

  def get_challenge_points(self):
    return self.attributes['LUM'] * self.max_damage / 2 + self.attributes['SIZ'] * health_per_con_point + self.AC

  def get_xp_worth(self):
    return int(self.get_challenge_points() / 4)

  def get_iron(self):
    return randint(round(self.xp_worth / 4), round(self.xp_worth / 2)) * 100

class WhiteDwarf(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 10,
      'SIZ' : 5,
      'VEL' : 10
    }
    super().__init__()
    self.AC = 10
    self.max_damage = 4
    self.name = "White Dwarf"
    self.xp_worth = self.get_xp_worth()
    self.iron = self.get_iron()

class GasGiant(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 12,
      'SIZ' : 7,
      'VEL' : 8
    }
    super().__init__()
    self.AC = 12
    self.max_damage = 5
    self.name = "Gas Giant"
    self.xp_worth = self.get_xp_worth()
    self.iron = self.get_iron()

class DarkMatter(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 14,
      'SIZ' : 11,
      'VEL' : 10
    }
    super().__init__()
    self.AC = 13
    self.max_damage = 7
    self.name = "Dark Matter"
    self.xp_worth = self.get_xp_worth()
    self.iron = self.get_iron()

class StellarWyrm(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 16,
      'SIZ' : 15,
      'VEL' : 8
    }
    super().__init__()
    self.AC = 16
    self.max_damage = 10
    self.name = "Stellar Wyrm"
    self.xp_worth = self.get_xp_worth()
    self.iron = self.get_iron()

class BlackHole(Monster):
  def __init__(self):
    self.attributes = {
      'LUM' : 18,
      'SIZ' : 25,
      'VEL' : 20
    }
    super().__init__()
    self.AC = 18
    self.max_damage = 12
    self.name = "Black Hole"
    self.xp_worth = self.get_xp_worth()
    self.iron = self.get_iron()

available_monsters = {
  WhiteDwarf  : 0.4,
  GasGiant    : 0.3,
  DarkMatter  : 0.2,
  StellarWyrm : 0.1
}
