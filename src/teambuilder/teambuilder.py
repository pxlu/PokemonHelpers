'''
1. Teambuilder to suggest coverage/strengths/weaknesses of teams
'''

import json
import itertools
import os
import re
import pprint
import glob
import math
from . import teambuilder_classes as tclass

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

PKMN_TYPES = {
  pkmn_type_name.upper(): tclass.PkmnType(name=pkmn_type_name, defense=pkmn_type_details['defense'], offense=pkmn_type_details['offense'])for (pkmn_type_name, pkmn_type_details) in TYPES_TABLE.items()
}

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

  return tclass.Pokemon(
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

def calculate_role_by_type_class(pokemon, role, role_moves):
  if any([move for move in pokemon.moveset], role_moves):
    return [move for move in pokemon.moveset if move in role_moves]
  return None

def classify_pkmn_by_role(pokemon):
  archetypes = {
    'utility': [
      'hazard_setter'
      'hazard_control',
      'cleric',
      'wish',
      'trick_room'
      'knock_off'
      'trick',
      'status',
      'healing_wish'
      'leech_seed',
      'screens',
      'pivot'
      'phazing'
    ], 
    'offensive': [
      'choice_band',
      'choice_scarf',
      'choice_specs',
      'setup_sweeper',
      'priority',
    ],
    'defensive': [
      'physical',
      'special',
      'mixed',
      'recovery',
    ],
    'weather': [
      'rain_setter',
      'sand_setter',
      'sun_setter',
      'hail_setter',
      'rain_user',
      'sand_user',
      'sun_user',
      'hail_user'
    ]
  }

  # RULES FOR CALCULATION
  # Utility
  # region Utility
  utility_rules_dict = {
    'hazards': ['spikes', 'toxic_spikes', 'stealth_rock', 'sticky_web'],
    'hazard_control': ['defog', 'rapid_spin'],
    'cleric': ['aromatherapy', 'heal_bell'],
    'trick_room': True if 'trick_room' in pokemon.moveset else False,
    'knock_off': True if 'knock_off' in pokemon.moveset else False,
    'trick': ['trick', 'switcharoo'],
    'status': ['sleep_powder', 'spore', 'will-o-wisp', 'thunder_wave', 'toxic', 'glare', 'stun_spore', 'zap_cannon', 'toxic_spikes', 'lovely_kiss', 'yawn', 'hypnosis'],
    'healing_wish': ['healing_wish', 'lunar_dance'],
    'leech_seed': True if 'leech_seed' in pokemon.moveset else False,
    'screens': ['reflect', 'light_screen', 'aurora_veil'],
    'phazing': ['whirlwind', 'roar', 'circle_throw', 'dragon_tail']
  }
  #endregion

  # Offensive
  # region Offensive
  pivot = ['u-turn', 'volt_switch', 'parting_shot', 'flip_turn', 'teleport']
  priority = ['fake_out', 'mach_punch', 'bullet_punch', 'ice_shard', 'sucker_punch', 'quick_attack', 'extremespeed', 'accelrock', 'shadow_sneak', 'vaccum_wave', 'water_shuriken', 'aqua_jet']
  choice_band = True if pokemon.item == 'choice_band' else False
  choice_scarf = True if pokemon.item == 'choice_scarf' else False
  choice_specs = True if pokemon.item == 'choice_specs' else False
  setup_sweeper = ['autotomize', 'belly_drum', 'bulk_up', 'calm_mind', 'dragon_dance', 'growth', 'nasty_plot', 'shell_smash', 'quiver_dance', 'shift_gear', 'agility', 'swords_dance', 'cosmic_power', 'acid_armor', 'cotton_guard', 'amnesia', 'geomancy', 'focus_energy', 'hone_claws', 'iron_defense', 'rock_polish', 'work_up', 'howl']
  #endregion

  # Defensive
  # region Defensive
  # Heuristics --
  # If def >= 25% after evs = physical
  # If spd >= 25% after evs = special
  # If 20% < def < 25% and 20% < spd < 25% = mixed
  physical = True if pokemon.stats['def'] >= 0.25 * sum([stat for stat in pokemon.stats.values()]) else False
  special = True if pokemon.stats['spd'] >= 0.25 * sum([stat for stat in pokemon.stats.values()]) else False
  mixed = True if 0.25 > pokemon.stats['def'] >= 0.20 * sum([stat for stat in pokemon.stats.values()]) and 0.25 > pokemon.stats['spd'] >= 0.20 * sum([stat for stat in pokemon.stats.values()]) else False
  recovery = ['milk_drink', 'recover', 'roost', 'shore_up', 'synthesis', 'morning_sun', 'rest', 'strength_sap', 'soft-boiled', 'moonlight', 'heal_order', 'slack_off']
  #endregion

  # Weather
  #region Weather
  sun_setter = True if pokemon.ability in ['drought', 'desolate_land'] else False
  sand_setter = True if pokemon.ability == 'sand_stream' else False
  rain_setter = True if pokemon.ability in ['drizzle', 'primordial_sea'] else False
  hail_setter = True if pokemon.ability == 'snow_warning' else False
  sun_user = True if pokemon.ability in ['chlorophyll', 'flower_gift', 'forecast', 'leaf_guard', 'solar_power'] else False
  rain_user = True if pokemon.ability in ['swift_swim', 'dry_skin', 'forecast', 'hydration', 'rain_dish'] else False
  sand_user = True if pokemon.ability in ['sand_rush', 'sand_force'] else False
  hail_user = True if pokemon.ability == 'slush_rush' else False
  #endregion

  roles = {
    'utility': {},
    'offensive': {},
    'defensive': {},
    'weather': {}
  }

  for util_role in archetypes['utility']:
    calculated_util_role = calculate_role_by_type_class(pokemon, util_role, utility_rules_dict['util_role'])
    if len(calculated_util_role) > 0:
      roles['utility'][util_role] = calculated_util_role

  #region Offensive Roles
  roles['offensive']['utility'] = None
  #endregion

def load_teamdata(team='sampleteam.txt'):
  print(os.getcwd())
  dex = open('../teambuilder/pokedex.json', encoding="utf8")
  # data.keys() is a list of pokemon names
  data = json.load(dex)
  
  sample_team = open('../teambuilder/sampleteam.txt', encoding="utf8").readlines()
  delimiter = '\n'
  # https://stackoverflow.com/questions/15357830/splitting-a-list-based-on-a-delimiter-word
  list_of_pokemon_data = [list(y) for x, y in itertools.groupby(sample_team, lambda z: z == delimiter) if not x]
  
  pkmn_list = []
  for pokemon in list_of_pokemon_data:
    pkmn = convert_pokemondata_into_pkmn(pokemon, data)
    pkmn_list.append(pkmn)

  return (pkmn_list, dex)

if __name__ == '__main__':
  (pkmn_list, dex) = load_teamdata()

  new_team = tclass.Team(roster=pkmn_list)
  for pkmn in new_team.roster:
    pkmn = calculate_pkmn_stats(pkmn)
  
  for pkmn in new_team.roster:
    print(pkmn.ability)
    classification = classify_pkmn_by_role(pkmn)
    print(classification)

  print(PKMN_TYPES['NORMAL'].defense)
  new_team._calculate_defensive_coverage()

  dex.close()