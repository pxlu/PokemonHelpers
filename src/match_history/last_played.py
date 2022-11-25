import psycopg2
from datetime import datetime
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
print(sys.path)

from common.db_config import config

def load_teamdata_from_match():
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
    cur.close()


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
