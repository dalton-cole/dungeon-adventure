#!/usr/bin/env python3

from print import slow_print
from random import randint, random


class Monster:
  def attack(self, player):
    if random() < self.accuracy:
      damage = randint(self.damage_lower, self.damage_upper)
      player.hp = max(0, player.hp - damage)
      slow_print(f'{self.name} does {damage} damage! Your remaining hit points are {player.hp}/{player.max_hp}!')
      if player.hp <= 0:
        slow_print('Your HP is depleted...Game Over!')
        exit()
    else:
      slow_print(f'{self.name} attacks and misses!')

class Goblin(Monster):
  def __init__(self):
    self.hp = 10
    self.accuracy = 0.6
    self.damage_lower = 1
    self.damage_upper = 3
    self.name = "Goblin"
    self.xp_worth = 30
    self.speed = 0.3

class DarkKnight(Monster):
  def __init__(self):
    self.hp = 16
    self.accuracy = 0.75
    self.damage_lower = 2
    self.damage_upper = 6
    self.name = "Dark Knight"
    self.xp_worth = 100
    self.speed = 0.4

class Dragon(Monster):
  def __init__(self):
    self.hp = 30
    self.accuracy = 0.85
    self.damage_lower = 6
    self.damage_upper = 12
    self.name = "Dragon"
    self.xp_worth = 1000
    self.speed = 0.7
