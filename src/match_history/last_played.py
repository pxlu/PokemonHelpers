from datetime import datetime
import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
print(sys.path)

def load_teamdata_from_match():
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
