'''
1. Teambuilder to suggest coverage/strengths/weaknesses of teams
'''

import json
import itertools

class Pokemon:
  def __init__(self, name=None, item=None, ability=None, evs=None, ivs=None, nature=None, moveset=None):
      self.name = name
      self.item = item,
      self.ability = ability
      self.evs = evs
      self.ivs = ivs
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
    pkmn_name, pkmn_item = pokemondata[0].split('@')[0], pokemondata[0].split('@')[-1] #e.g Suicune @ Leftovers
    pkmn_ability = pokemondata[1].split(':')[1].strip() #e.g Pressure
    
    pkmn_evs_data = [x.strip() for x in  pokemondata[2].split(':')[-1].split('/')]
    print(pkmn_name)
    for p in pkmn_evs_data:
      print(p)
    #print(pokemondata[2].split(':')[-1].split('/'))
    #pkmn_evs = pokemondata[2].split(':')
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