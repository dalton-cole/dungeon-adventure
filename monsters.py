#!/usr/bin/env python3

from print import slow_print
from random import randint, random


health_per_con_point = 3

class Monster:
  def get_attribute_modifier(self, attr):
    return self.attributes[attr] - 10

  def attack(self, player):
    if randint(1, 20) + self.get_attribute_modifier('STR') >= player.get_AC():
      damage = self.roll_damage() + self.get_attribute_modifier('STR')
      player.hp = max(0, player.hp - damage)
      slow_print(f'{self.name} does {damage} damage! Your remaining hit points are {player.hp}/{player.max_hp}!')
      if player.hp <= 0:
        slow_print('Your HP is depleted...Game Over!')
        exit()
    else:
      slow_print(f'{self.name} attacks and misses!')

  def roll_initiative(self):
    return randint(1, 20) + self.get_attribute_modifier('DEX')

  def roll_damage(self):
    return randint(1, self.max_damage) + self.get_attribute_modifier('STR')

  def assign_max_hp(self):
    self.max_hp = self.attributes['CON'] * health_per_con_point

class Goblin(Monster):
  def __init__(self):
    self.attributes = {
      'STR' : 10,
      'INT' : 5,
      'CON' : 4,
      'DEX' : 8
    }
    self.hp = self.attributes['CON'] * health_per_con_point
    self.assign_max_hp()
    self.AC = 10
    self.max_damage = 4
    self.name = "Goblin"
    self.xp_worth = 30

class DarkKnight(Monster):
  def __init__(self):
    self.attributes = {
      'STR' : 12,
      'INT' : 10,
      'CON' : 6,
      'DEX' : 10
    }
    self.hp = self.attributes['CON'] * health_per_con_point
    self.assign_max_hp()
    self.AC = 14
    self.max_damage = 6
    self.name = "Dark Knight"
    self.xp_worth = 100

class Dragon(Monster):
  def __init__(self):
    self.attributes = {
      'STR' : 16,
      'INT' : 12,
      'CON' : 10,
      'DEX' : 12
    }
    self.hp = self.attributes['CON'] * health_per_con_point
    self.assign_max_hp()
    self.AC = 18
    self.max_damage = 12
    self.name = "Dragon"
    self.xp_worth = 1000
