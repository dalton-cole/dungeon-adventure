#!/usr/bin/env python3

from random import randint


class AttackSpell:
  def __init__(self):
    self.is_consumable = False

  def roll_damage(self):
    return randint(1, self.max_damage)

  def describe(self):
    return f'Attack spell deals 1d{self.max_damage} DMG [{self.range} target]'

class SolarFlare(AttackSpell):
  def __init__(self):
    super().__init__()
    self.max_damage = 8
    self.name = 'Solar Flare'
    self.range = 'single'

class Eclipse(AttackSpell):
  def __init__(self):
    super().__init__()
    self.max_damage = 10
    self.name = 'Eclipse'
    self.range = 'multiple'
    self.price = 1000

class Supernova(AttackSpell):
  def __init__(self):
    super().__init__()
    self.max_damage = 20
    self.name = 'Supernova'
    self.range = 'single'
    self.price = 8000
