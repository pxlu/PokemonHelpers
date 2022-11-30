import psycopg2
from datetime import datetime
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from common.db_config import config

def connect_to_db():
    # read connection parameters
    params = config()

    # connect to the PostgreSQL server
    print('Connecting to the PostgreSQL database...')
    conn = psycopg2.connect(**params)

    # create a cursor
    cur = conn.cursor()

    # execute a statement
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

    # close the communication with the PostgreSQL
    # cur.close()

    return cur

def load_teamdata_from_match(db_cursor, player_1_name, player_2_name):

  """
  First, get the match_id from match_history
  Then, match that match_id with the match_id from the match_history_teams table
  Then, for each pokemon for both players, get all known moves, items and abilities, shininess, level, gender for each pokemon
    For your own team's pokemon, also get the EVs and IVs for each pokemon

  """
  SQL = '''
    SELECT * FROM match_history
    WHERE player1 
  '''

  return None


def last_played():

    # Fetch data from the last played match for user here...
    # 1. Auth the user
    # 2. Query db to get last played match by datetime
    # 3. Return the match history as a json

    last_match_data = {
        'format': 'gen8ou',
        'turnsElapsed': 40,
        'match_datetime': datetime.fromisoformat('2011-11-04T00:05:23Z'),
        'result': {
            'player1': 'win',
            'player2': 'loss'
        },
        'player1': {
            'name': 'p1',
            'elo': 1400,
            'team': load_teamdata_from_match()
        }, 'player2': {
            'name': 'p2',
            'elo': 1400,
            'team': load_teamdata_from_match()
        }, 'match_log': None
    }

    return None


if __name__ == '__main__':
    load_teamdata_from_match()
