import requests
import json
import os
import time


# Get a specific league
def get_league(league_id):
    '''
    Get json data from "Get a specific league" endpoint of the Sleeper API.

    :param league_id: Unique league identifier provided by the Sleeper API.
    :return:
    '''
    url = f'https://api.sleeper.app/v1/league/{league_id}'
    r = requests.get(url, timeout=10)

    json_data = r.json()

    return json_data

# Getting rosters in a league
def get_rosters(league_id):
    '''
    Get json data from rosters endpoint of the Sleeper API.

    :param league_id: Unique league identifier provided by the Sleeper API.
    :return:
    '''
    url = f"https://api.sleeper.app/v1/league/{league_id}/rosters"
    r = requests.get(url, timeout=100)

    json_data = r.json()

    return json_data

# Getting users in a league
def get_user_info(league_id):
    '''
    Get json data from "Getting users in a league" endpoint of the Sleeper API.

    :param league_id: Unique league identifier provided by the Sleeper API.
    :return:
    '''
    url = f"https://api.sleeper.app/v1/league/{league_id}/users"
    r = requests.get(url, timeout=10)

    json_data = r.json()

    return json_data

# Getting matchups in a league
def get_matchups(week, league_id):
    '''
    Get json data from "Getting matchups in a league" endpoint of the Sleeper API.

    :param week: The week number of the nfl season.
    :param league_id: Unique league identifier provided by the Sleeper API.
    :return:
    '''
    valid_weeks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    if week in valid_weeks:
        url = f"https://api.sleeper.app/v1/league/{league_id}/matchups/{week}"
        r = requests.get(url, timeout=100)

        json_data = r.json()
        return json_data

    raise ValueError('Invalid week passed. Week must be an integer greater than or equal to one and less than eighteen.')

# Get transactions
def get_transactions(week, league_id):
    '''
    Get json data from "Get transactions" endpoint of the Sleeper API.
    
    :param week: The week number of the nfl season.
    :param league_id: Unique league identifier provided by the Sleeper API.
    :return: 
    '''
    url = f'https://api.sleeper.app/v1/league/{league_id}/transactions/{week}'
    r = requests.get(url, timeout=20)

    json_data = r.json()

    return json_data

# Get NFL state
def get_nfl_state():
    '''
    Get json data from "Get NFL state" endpoint of the Sleeper API.
    
    :return: 
    '''
    url = f"https://api.sleeper.app/v1/state/nfl"
    r = requests.get(url, timeout=5)

    json_data = r.json()

    return json_data

# Get a specific draft
def get_draft_info(draft_id):
    '''
    Get json data from "Get a specific draft" endpoint of the Sleeper API.
    
    :param draft_id: Unique draft identifier provided by the Sleeper API.
    :return: 
    '''
    url = f"https://api.sleeper.app/v1/draft/{draft_id}"
    r = requests.get(url, timeout=10)

    json_data = r.json()

    return json_data

# Get all picks in a draft
def get_draft_picks(draft_id):
    '''
    Get json data from "Get all picks in a draft" endpoint of the Sleeper API.
    
    :param draft_id: Unique draft identifier provided by the Sleeper API.
    :return: 
    '''
    url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
    r = requests.get(url, timeout=10)

    json_data = r.json()

    return json_data

# Fetch all players
def get_player_data():
    '''
    Get json data from "Get all picks in a draft" endpoint of the Sleeper API.

    Only run this API call once per day.
    
    :return: 
    '''
    url = r"https://api.sleeper.app/v1/players/nfl"
    r = requests.get(url, timeout=100)
    json_data = r.json()

    return json_data


def save_json_file(json_object, file_name):
    '''
    This function writes json data to a file.
    
    :param json_object: 
    :param file_name: 
    :return: 
    '''
    with open(file_name, "w") as outfile:
        json.dump(json_object, outfile)

def extract_all(directory,
                api_params={'league_id':'858131629682577408',
                            'draft_id':'983048181460119553',
                            'week': 1},
                include_player_data=True):
    '''Call all "get" functions and save their output_data to a specified directory.'''

    t0 = time.time()
    num_weeks = 18

    json_objects = []
    json_names = ['user_info', 'nfl_state', 'rosters', 'draft_info', 'draft_picks', 'league', 'transactions']  # Exclude player data
    json_names = ['user_info', 'player_data', 'nfl_state', 'rosters', 'draft_info', 'draft_picks', 'league',
    'transactions']

    json_objects.append(get_user_info(league_id=api_params['league_id']))
    json_objects.append(get_player_data())
    json_objects.append(get_nfl_state())
    json_objects.append(get_rosters(league_id=api_params['league_id']))
    json_objects.append(get_draft_info(draft_id=api_params['draft_id']))
    json_objects.append(get_draft_picks(draft_id=api_params['draft_id']))
    json_objects.append(get_league(league_id=api_params['league_id']))
    json_objects.append(get_transactions(week=api_params['week'], league_id=api_params['league_id']))

    for i in range(1, num_weeks + 1):
        json_objects.append(get_matchups(week=i, league_id=api_params['league_id']))
        json_names.append('matchups_week_' + "{:02d}".format(
            i))  # DO NOT CHANGE! The naming convention is necessary for the Transform.transform_roster_weeks function

    t1 = time.time()
    print(t1 - t0, " seconds to extract data from the Sleeper API.")

    # Save json objects to a specified directory
    for json_object, json_name in zip(json_objects, json_names):
        filepath = os.path.join(directory, json_name + '.json')
        save_json_file(json_object, filepath)
