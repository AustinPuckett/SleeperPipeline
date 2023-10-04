import extract
import transform
import load
import os
import time


def run_sleeper_etl(db, week, api_params, inlcude_player_data=True):
  #TODO: remove hard coded api params
  
  num_weeks=18
  
  table_names = ['league', 'roster', 'rostered_player', 'user', 'roster_week', 'player_week', 'league_transaction',
                 'nfl_state', 'draft_info', 'draft_pick', 'draft_order', 'player']
  

  api_params={'league_id':'983048181460119552',
                              'draft_id':'983048181460119553'}
  
  api_params['week'] = week
  
  json_dict = extract.extract_all(api_params=api_params, include_player_data=inlcude_player_data)   # Call Sleeper API to get json data
  table_entries_dict = transform.transform_many(table_names, json_dict)
  
  api = load.FantasyApi(db)
  api.update_tables(table_entries_dict, _overwrite=True)
