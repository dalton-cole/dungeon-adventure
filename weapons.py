#!/usr/bin/env python3

from random import randint
from print import slow_print
from items import Item


class MeleeWeapon(Item):
  def __init__(self):
    self.is_consumable = False

  def roll_damage(self):
    return randint(1, self.max_damage)

  def use(self, player):
    player.equipped_weapon = self
    slow_print(f'You have equipped {self.name}.')

  def is_usable(self, player):
    return True

class StarShard(MeleeWeapon):
  def __init__(self):
    super().__init__()
    self.max_damage = 6
    self.attack_bonus = 1
    self.name = "Star Shard"
    self.price = 200

class VegaBlade(MeleeWeapon):
  def __init__(self):
    super().__init__()
    self.max_damage = 10
    self.attack_bonus = 2
    self.name = "Vega Blade"
    self.price = 1000

class CygnusHammer(MeleeWeapon):
  def __init__(self):
    super().__init__()
    self.max_damage = 14
    self.attack_bonus = 4
    self.name = "Cygnus Hammer"
    self.price = 5000
