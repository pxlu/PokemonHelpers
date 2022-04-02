'''
1. Teambuilder to suggest coverage/strengths/weaknesses of teams
'''

import json
import itertools
import re
import pprint

class Pokemon:
  def __init__(self, name=None, item=None, ability=None, evs=None, ivs=None, stats=None, level=None, nature=None, moveset=None):
    self.name = name
    self.item = item,
    self.ability = ability
    self.evs = evs
    self.ivs = ivs
    self.stats = stats
    self.level = level
    self.nature = nature
    self.moveset = moveset

  def __str__(self):
    level_string = 'Level: ' + self.level + '\n' if self.level else ''
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
    if iv_string.strip()[-1] == '/':
      iv_string = iv_string[:-2]
    moveset_string = ''
    for move in self.moveset:
      moveset_string += '- ' + move +'\n'
    moveset_string = moveset_string.strip()

    return self.name + ' @ ' + self.item[0] + '\n' + 'Ability: ' + self.ability + '\n' + level_string + ev_string + '\n' + self.nature + ' Nature\n' + iv_string + '\n' + moveset_string
  
class Team:
  def __init__(self, roster=None):
    self.roster = roster

def calculate_pkmn_stats(pokemon):
  pass

def convert_pokemondata_into_pkmn(pokemondata):

  pokemondata = [x.strip() for x in pokemondata]
  name_item_pattern = re.compile('.+ @ .+')
  ability_pattern, nature_pattern = re.compile('Ability: .+'), re.compile('[a-zA-Z]+ Nature')
  evs_pattern, ivs_pattern = re.compile('EVs: .+'), re.compile('IVs: .+')
  level_pattern, shiny_pattern = re.compile('Level: .+'), re.compile('Shiny: .+')
  moveset_pattern = re.compile('- .+')

  pkmn_name, pkmn_item, pkmn_ability, pkmn_nature, pkmn_level = None, None, None, None, None 
  pkmn_evs, pkmn_ivs = {'HP': 0, 'Atk': 0, 'Def': 0, 'SpA': 0, 'SpD': 0, 'Spe': 0}, {'HP': 31, 'Atk': 31, 'Def': 31, 'SpA': 31, 'SpD': 31, 'Spe': 31}
  pkmn_moveset = []

  for pattern in pokemondata:
    name_item_match, ability_pattern_match, nature_pattern_match = name_item_pattern.match(pattern), ability_pattern.match(pattern), nature_pattern.match(pattern)
    evs_pattern_match, ivs_pattern_match = evs_pattern.match(pattern), ivs_pattern.match(pattern)
    level_pattern_match, shiny_pattern_match = level_pattern.match(pattern), shiny_pattern.match(pattern)
    moveset_pattern_match = moveset_pattern.match(pattern)

    if name_item_match:
      pkmn_name, pkmn_item = name_item_match.group(0).split('@')[0].strip(), name_item_match.group(0).split('@')[-1].strip()
    if ability_pattern_match:
      pkmn_ability = ability_pattern_match.group(0).split(':')[1].strip()
    if nature_pattern_match:
      pkmn_nature = nature_pattern_match.group(0).split(' ')[0].strip()
    if evs_pattern_match:
      pkmn_evs_data = [x.strip() for x in evs_pattern_match.group(0).split(':')[-1].split('/')]
      for ev_pair in pkmn_evs_data:
        pkmn_evs[ev_pair.split(' ')[-1]] = int(ev_pair.split(' ')[0])
    if ivs_pattern_match:
      pkmn_ivs_data = [x.strip() for x in ivs_pattern_match.group(0).split(':')[-1].strip().split('/')]
      for iv_pair in pkmn_ivs_data:
        pkmn_ivs[iv_pair.split(' ')[-1]] = int(iv_pair.split(' ')[0])
    if level_pattern_match:
      pkmn_level = level_pattern_match.group(0).split(':')[-1].strip()
    if moveset_pattern_match:
      pkmn_moveset.append(moveset_pattern_match.group(0)[2:].strip())

  return Pokemon(
    name = pkmn_name,
    item = pkmn_item,
    ability = pkmn_ability,
    evs = pkmn_evs,
    ivs = pkmn_ivs,
    level = pkmn_level,
    nature = pkmn_nature,
    moveset = pkmn_moveset
  )

if __name__ == '__main__':
  dex = open('pokedex.json', encoding="utf8")
  # data.keys() is a list of pokemon names
  data = json.load(dex)
  
  sample_team = open('sampleteam.txt', encoding="utf8").readlines()
  delimiter = '\n'
  # https://stackoverflow.com/questions/15357830/splitting-a-list-based-on-a-delimiter-word
  list_of_pokemon_data = [list(y) for x, y in itertools.groupby(sample_team, lambda z: z == delimiter) if not x]
  
  pkmn_list = []
  for pokemon in list_of_pokemon_data:
    pkmn = convert_pokemondata_into_pkmn(pokemon)
    pkmn_list.append(pkmn)

  new_team = Team(roster=pkmn_list)
  print(new_team.roster[0])

  dex.close()