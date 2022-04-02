'''
1. Teambuilder to suggest coverage/strengths/weaknesses of teams
'''

import json
import itertools
import re

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
  
class Team:
  def __init__(self, roster=None):
    self.roster = roster

  def _import_team():
    # Need to convert team text file into a list of pokemon object
    '''
    
    '''
    pass

def convert_pokemondata_into_pkmn(pokemondata):

    pokemondata = [x.strip() for x in pokemondata]
    name_item_pattern = re.compile('.+ @ .+')
    ability_pattern, nature_pattern = re.compile('Ability: .+'), re.compile('[a-zA-Z]+ Nature')

    for pattern in pokemondata:
      name_item_match, ability_pattern_match, nature_pattern_match = name_item_pattern.match(pattern), ability_pattern.match(pattern), nature_pattern.match(pattern)
      if name_item_match:
        pkmn_name, pkmn_item = name_item_match.group(0).split('@')[0], name_item_match.group(0).split('@')[-1]
      if ability_pattern_match:
        pkmn_ability = ability_pattern_match.group(0).split(':')[1]
      if nature_pattern_match:
        pkmn_nature = nature_pattern_match.group(0).split(' ')[0]

    pkmn_evs = {'HP': 0, 'Atk': 0, 'Def': 0, 'SpA': 0, 'SpD': 0, 'Spe': 0}
    pkmn_evs_data = [x.strip() for x in pokemondata[2].split(':')[-1].split('/')] #e.g EVs: 252 HP / 40 Def / 216 Spe
    for ev_pair in pkmn_evs_data:
      pkmn_evs[ev_pair.split(' ')[-1]] = int(ev_pair.split(' ')[0])
    
    pkmn_ivs = {'HP': 31, 'Atk': 31, 'Def': 31, 'SpA': 31, 'SpD': 31, 'Spe': 31}
    pkmn_ivs_data = [x.strip() for x in pokemondata[4].split(':')[-1].strip().split('/') if pokemondata[4].strip()[0:2] == 'IV'] 
    for iv_pair in pkmn_ivs_data:
      pkmn_ivs[iv_pair.split(' ')[-1]] = int(iv_pair.split(' ')[0])
    # npkmn = Pokemon(
    #   name=pkmn_name
    # )
    # return npkmn
    return Pokemon()

if __name__ == '__main__':
  dex = open('pokedex.json', encoding="utf8")
  data = json.load(dex)
  
  sample_team = open('sampleteam.txt', encoding="utf8").readlines()
  delimiter = '\n'
  # https://stackoverflow.com/questions/15357830/splitting-a-list-based-on-a-delimiter-word
  list_of_pokemon_data = [list(y) for x, y in itertools.groupby(sample_team, lambda z: z == delimiter) if not x]
  for pokemon in list_of_pokemon_data:
    pkmn = convert_pokemondata_into_pkmn(pokemon)
    #print(pkmn.name)
  # data.keys() is a list of pokemon names
  dex.close()