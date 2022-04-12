'''
1. Teambuilder to suggest coverage/strengths/weaknesses of teams
'''

import json
import itertools
import re
import pprint
import math

# 1: +10%, -1: -10%
NATURES_TABLE = {
  'hardy': None,
  'lonely': {'atk': 1, 'def': -1},
  'brave': {'atk': 1, 'spe': -1},
  'adamant': {'atk': 1, 'spa': -1},
  'naughty': {'atk': 1, 'spd': -1},
  'bold': {'def': 1, 'atk': -1},
  'docile': None,
  'impish': {'def': 1, 'spa': -1},
  'lax': {'def': 1, 'spd': -1},
  'relaxed': {'def': 1, 'spd': -1},
  'modest': {'atk': -1, 'spa': 1},
  'mild': {'def': -1, 'spa': 1},
  'bashful': None,
  'rash': {'spa': 1, 'spd': -1},
  'quiet': {'spa': 1, 'spe': -1},
  'calm': {'atk': -1, 'spd': 1},
  'gentle': {'def': -1, 'spd': 1},
  'careful': {'spa': -1, 'spd': 1},
  'quirky': None,
  'sassy': {'spd': 1, 'spe': -1},
  'timid': {'atk': 1, 'spe': 1},
  'hasty': {'def': -1, 'spe': 1},
  'jolly': {'spa': -1, 'spe': 1},
  'naive': {'spd': -1, 'spe': 1},
  'serious': None
}

# 0 on defense means immune to, 0 on offensive means cannot effect, 2 on defense means weak to, 2 on offensive means super-effective,
# 0.5 on defense means resist, 0.5 on offense means not very effective
TYPES_TABLE = { 
  'normal': {'defense': {'ghost': 0, 'fighting': 2}, 'offense': {'ghost': 0}},
  'fighting': {'defense': {'flying': 2, 'rock': 0.5, 'bug': 0.5, 'psychic': 2, 'dark': 0.5, 'fairy': 2}, 'offense': {'normal': 2, 'flying': 0.5, 'poison': 0.5, 'rock': 2, 'bug': 0.5, 'ghost': 0, 'steel': 2, 'psychic': 0.5, 'ice': 2, 'dark': 2, 'fairy': 0.5}},
  'flying': {'defense': {'fighting': 0.5, 'ground': 0, 'rock': 2, 'bug': 0.5, 'grass': 0.5, 'electric': 2, 'ice': 2}, 'offense': {'fighting:': 2, 'rock': 0.5, 'bug': 2, 'steel': 0.5, 'grass': 2, 'electric': 0.5}},
  'poison': {'defense': {'fighting': 0.5, 'poison': 0.5, 'ground': 2, 'bug': 0.5, 'grass': 0.5, 'psychic': 2, 'fairy': 0.5}, 'offense': {'poison': 0.5, 'rock': 0.5, 'ground': 0.5, 'steel': 0, 'grass': 2, 'fairy': 2}},
  'ground': {'defense': {'poison': 2, 'rock': 0.5, 'water': 2, 'grass': 2, 'electric': 0, 'ice': 2}, 'offense': {'flying': 0, 'poison': 2, 'rock': 2, 'bug': 0.5, 'steel': 2, 'fire': 2, 'grass': 0.5, 'electric': 2}},
  'rock': {'defense': {'normal': 0.5, 'fighting': 2, 'flying': 0.5, 'poison': 0.5, 'ground': 2, 'steel': 2, 'fire': 0.5, 'water': 2, 'grass': 2}, 'offense': {'fighting': 0.5, 'flying': 2, 'ground': 0.5, 'bug': 2, 'steel': 0.5, 'fire': 2, 'ice': 2}},
  'bug': {'defense': {'fighting': 0.5, 'flying': 2, 'ground': 0.5, 'rock': 2, 'fire': 2, 'grass': 0.5}, 'offense': {'fighting': 0.5, 'flying': 0.5, 'poison': 0.5, 'ghost': 0.5, 'steel': 0.5, 'fire': 0.5, 'grass': 2, 'psychic': 2, 'dark': 2, 'fairy': 0.5}},
  'ghost': {'defense': {'normal': 0, 'fighting': 0, 'poison': 0.5, 'bug': 0.5, 'ghost': 2, 'dark': 2}, 'offense': {'normal': 0, 'ghost': 2, 'psychic': 2, 'dark': 0}},
  'steel': {'defense': {'normal': 0.5, 'fighting': 2, 'flying': 0.5, 'poison': 0, 'ground': 2, 'rock': 0.5, 'bug': 0.5, 'steel': 0.5, 'fire': 2, 'grass': 0.5, 'psychic': 0.5, 'ice': 0.5, 'dragon': 0.5, 'fairy': 0.5}, 'offense': {'rock': 2, 'steel': 0.5, 'fire': 0.5, 'water': 0.5, 'electric': 0.5, 'ice': 2, 'fairy': 2}},
  'fire': {'defense': {'ground': 2, 'rock': 2, 'water': 2, 'bug': 0.5, 'steel': 0.5, 'ice': 0.5, 'grass': 0.5, 'fire': 0.5, 'fairy': 0.5}, 'offense': {'rock': 0.5, 'bug': 2, 'steel': 2, 'water': 0.5, 'fire': 0.5, 'grass': 2, 'ice': 2, 'dragon': 0.5}},
  'water': {'defense': {'steel': 0.5, 'fire': 0.5, 'water': 0.5, 'electric': 2, 'grass': 2, 'ice': 0.5}, 'offense': {'ground': 2, ' rock': 2, 'fire': 2, 'water': 0.5, 'grass': 0.5, 'dragon': 0.5}},
  'grass': {'defense': {'flying': 2, 'poison': 2, 'ground': 0.5, 'bug': 2, 'fire': 2, 'water': 0.5, 'electric': 0.5, 'grass': 0.5, 'ice': 2}, 'offense': {'flying': 0.5, 'poison': 0.5, 'ground': 2, 'rock': 2, 'bug': 0.5, 'steel': 0.5, 'fire': 0.5, 'water': 2, 'grass': 0.5, 'dragon': 0.5}},
  'electric': {'defense': {'flying': 0.5, 'ground': 2, 'steel': 0.5, 'electric': 0.5}, 'offense': {'flying': 2, 'ground': 0, 'water': 2, 'grass': 0.5, 'electric': 0.5, 'dragon': 0.5}},
  'psychic': {'defense': {'fighting': 0.5, 'bug': 2, 'ghost': 2, 'psychic': 0.5, 'dark': 2}, 'offense': {'fighting': 2, 'poison': 2, 'dark': 0, 'steel': 0.5, 'psychic': 0.5}},
  'ice': {'defense': {'fighting': 2, 'rock': 2, 'steel': 2, 'fire': 2, 'ice': 0.5}, 'offense': {'flying': 2, 'ground': 2, 'steel': 0.5, 'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 0.5, 'dragon': 2}},
  'dragon': {'defense': {'water': 0.5, 'fire': 0.5, 'grass': 0.5, 'electric': 0.5, 'ice': 2, 'dragon': 2, 'fairy': 2}, 'offense':{'steel': 0.5, 'dragon': 2, 'fairy': 0}},
  'dark': {'defense': {'fighting': 2, 'bug': 2, 'ghost': 0.5, 'psychic': 0, 'dark': 0.5, 'fairy': 2}, 'offense': {'fighting': 0.5, 'ghost': 2, 'psychic': 2, 'dark': 0.5, 'fairy': 0.5}},
  'fairy': {'defense': {'fighting': 0.5, 'dark': 0.5, 'bug': 0.5, 'dragon': 0, 'steel': 2, 'poison': 2}, 'offense': {'fighting': 2, 'poison': 0.5, 'steel': 0.5, 'fire': 0.5, 'dragon': 2, 'dark': 2}}
}

class PkmnType:
  def __init__(self, name, defense, offense):
    self.name = name
    self.defense = defense
    self.offense = offense

PKMN_TYPES = {
  pkmn_type_name.upper(): PkmnType(name=pkmn_type_name, defense=pkmn_type_details['defense'], offense=pkmn_type_details['offense'])for (pkmn_type_name, pkmn_type_details) in TYPES_TABLE.items()
}

class Pokemon:
  def __init__(self, name=None, item=None, ability=None, evs=None, ivs=None, stats=None, level=None, nature=None, moveset=None, dex_data=None):
    self.name = name
    self.item = item
    self.ability = ability
    self.evs = evs
    self.ivs = ivs
    self.stats = stats
    self.level = 100 if not level else level
    self.nature = nature
    self.moveset = moveset
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

    print(roster_types)
    return roster_types

def dex_lookup(dex, pokemon_name):
  return dex[pokemon_name.lower()]

def pokemon_nature_calculation(nature, stat):
  if stat.lower() in NATURES_TABLE[nature.lower()]:
    if NATURES_TABLE[nature.lower()][stat.lower()] > 0:
      return 1.1
    else:
      return 0.9
  else:
    return 1

def normal_stat_formula(pokemon_data, stat, nature):
  # (((IV + 2 * BaseStat + (EV/4) ) * Level/100 ) + 5) * Nature Value
  inner_stat_value = (2 * pokemon_data.dex_data['baseStats'][stat]) + pokemon_data.ivs[stat] + (pokemon_data.evs[stat] / 4)
  return math.floor((inner_stat_value * pokemon_data.level / 100 + 5) * pokemon_nature_calculation(nature, stat))

def calculate_pkmn_stats(pokemon):
  hp_formula_calculation = ((pokemon.ivs['hp'] + 2 * pokemon.dex_data['baseStats']['hp'] + (pokemon.evs['hp']/4)) * pokemon.level/100) + 10 + pokemon.level

  pokemon.stats = {
    'hp': hp_formula_calculation,
    'atk': normal_stat_formula(pokemon, 'atk', pokemon.nature),
    'def': normal_stat_formula(pokemon, 'def', pokemon.nature),
    'spa': normal_stat_formula(pokemon, 'spa', pokemon.nature),
    'spd': normal_stat_formula(pokemon, 'spd', pokemon.nature),
    'spe': normal_stat_formula(pokemon, 'spe', pokemon.nature),
  }

  return pokemon

def normalize_pokemon_name(pokemon_name):
  return ''.join(pokemon_name.lower().split('-'))

def convert_pokemondata_into_pkmn(pokemondata, dex):

  pokemondata = [x.strip() for x in pokemondata]
  name_item_pattern = re.compile('.+ @ .+')
  ability_pattern, nature_pattern = re.compile('Ability: .+'), re.compile('[a-zA-Z]+ Nature')
  evs_pattern, ivs_pattern = re.compile('EVs: .+'), re.compile('IVs: .+')
  level_pattern, shiny_pattern = re.compile('Level: .+'), re.compile('Shiny: .+')
  moveset_pattern = re.compile('- .+')

  pkmn_name, pkmn_item, pkmn_ability, pkmn_nature, pkmn_level = None, None, None, None, None 
  pkmn_evs, pkmn_ivs = {'hp': 0, 'atk': 0, 'def': 0, 'spa': 0, 'spd': 0, 'spe': 0}, {'hp': 31, 'atk': 31, 'def': 31, 'spa': 31, 'spd': 31, 'spe': 31}
  pkmn_moveset = []

  for pattern in pokemondata:
    name_item_match, ability_pattern_match, nature_pattern_match = name_item_pattern.match(pattern), ability_pattern.match(pattern), nature_pattern.match(pattern)
    evs_pattern_match, ivs_pattern_match = evs_pattern.match(pattern), ivs_pattern.match(pattern)
    level_pattern_match, shiny_pattern_match = level_pattern.match(pattern), shiny_pattern.match(pattern)
    moveset_pattern_match = moveset_pattern.match(pattern)

    if name_item_match:
      pkmn_name, pkmn_item = name_item_match.group(0).split('@')[0].strip().split(' ')[0].strip(), name_item_match.group(0).split('@')[-1].strip()
    if ability_pattern_match:
      pkmn_ability = ability_pattern_match.group(0).split(':')[1].strip()
    if nature_pattern_match:
      pkmn_nature = nature_pattern_match.group(0).split(' ')[0].strip()
    if evs_pattern_match:
      pkmn_evs_data = [x.strip() for x in evs_pattern_match.group(0).split(':')[-1].split('/')]
      for ev_pair in pkmn_evs_data:
        pkmn_evs[ev_pair.split(' ')[-1].lower()] = int(ev_pair.split(' ')[0])
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
    moveset = pkmn_moveset,
    dex_data = dex_lookup(dex, normalize_pokemon_name(pkmn_name))
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
    pkmn = convert_pokemondata_into_pkmn(pokemon, data)
    pkmn_list.append(pkmn)

  new_team = Team(roster=pkmn_list)
  for pkmn in new_team.roster:
    pkmn = calculate_pkmn_stats(pkmn)
  
  for pkmn in new_team.roster:
    print(pkmn.stats)

  print(PKMN_TYPES['NORMAL'].defense)
  new_team._calculate_defensive_coverage()

  dex.close()