
import json
import itertools
import re
import pprint
import math

class PkmnType:
  def __init__(self, name, defense, offense):
    self.name = name
    self.defense = defense
    self.offense = offense

class Pokemon:
  def __init__(self, name=None, item=None, ability=None, evs=None, ivs=None, stats=None, level=None, nature=None, moveset=None, dex_data=None):
    self.name = name
    self.item = item.strip().lower().replace(' ', '_')
    self.ability = ability.strip().lower().replace(' ', '_')
    self.evs = evs
    self.ivs = ivs
    self.stats = stats
    self.level = 100 if not level else level
    self.nature = nature
    self.moveset = [move.strip().lower().replace(' ', '_') for move in moveset]
    self.dex_data = dex_data

  def __str__(self):
    level_string = 'Level: ' + str(self.level) + '\n' if self.level else ''
    ev_string = 'EVs: ' 
    for ev_stat in self.evs.keys():
      ev_number = self.evs[ev_stat]
      if ev_number > 0:
        ev_string += str(ev_number) + ' ' + ev_stat + ' / '
    if ev_string.strip()[-1] == '/':
      ev_string = ev_string[:-2]
    iv_string = ''
    for k,v in self.ivs.items():
      if v != 31:
        if iv_string == '':
          iv_string = 'IVs: '
        iv_string += str(v) + ' ' + k + ' / ' 
    if iv_string and iv_string.strip()[-1] == '/':
      iv_string = iv_string[:-2]
    moveset_string = ''
    for move in self.moveset:
      moveset_string += '- ' + move +'\n'
    moveset_string = moveset_string.strip()

    return self.name + ' @ ' + self.item + '\n' + 'Ability: ' + self.ability + '\n' + level_string + ev_string + '\n' + self.nature + ' Nature\n' + iv_string + '\n' + moveset_string

class Team:
  def __init__(self, roster=None):
    self.roster = roster

  def _calculate_defensive_coverage(self):
    roster_types = {}
    for pkmn in self.roster:
      for pkmn_type in pkmn.dex_data['types']:
        if pkmn_type not in roster_types.keys():
          roster_types[pkmn_type.lower()] = 1
        else:
          roster_types[pkmn_type.lower()] += 1

    return roster_types