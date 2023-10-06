import os
import json
import sqlite3 as sql
import analysis.standard_queries as standard_queries
import pipeline.sleeper_etl as sleeper_etl

class AccountModel():
    '''TODO: Change working directory once this program is converted to a .exe'''

    def __init__(self):
        self.root_path = os.path.join(os.getcwd(), 'app')
        print(self.root_path)
        self.config_file_name = 'config.txt'
        self.config_file_name_path = os.path.join(self.root_path, self.config_file_name)
        self.download_file_path = None
        self.db_conn = None
        self.username = None
        self.league_id = None
        self.draft_ids = None

        # Check if config file exists
        config_exists = False
        for file in os.listdir(self.root_path):
            if file == self.config_file_name:
                config_exists = True
        if config_exists == False:
            with open(self.config_file_name_path, 'w') as config_file:
                print('Successfully created config file.')

        # Check if config file is empty or corrupted
        config_empty = True
        config_corrupted = False
        with open(self.config_file_name_path, 'r') as config_file:
            pass

    def validate_login(self, username):
        login_response = {'success': False, 'message': None}
        with open(self.config_file_name_path, 'r') as config_file:
            for row in config_file:
                account_info = json.loads(row)
                if username == account_info['username']:
                    database = account_info['database']
                    self.db_conn = standard_queries.connect_to_db(database)
                    self.username = username
                    # self.league_id = account_info['league_id']
                    # self.draft_ids = account_info['draft_ids']
                    login_response['success'] = True
                    return login_response

        login_response['message'] = 'There was an unexpected error. Check the configuration file to see if the ' \
                                    'username exists.'
        return login_response

    def get_usernames(self):
        '''Access the entries in the configuration file.'''
        account_list = []
        with open(self.config_file_name_path, 'r') as config_file:
            for row in config_file:
                account_list.append(json.loads(row))

        usernames = [account['username'] for account in account_list]

        return usernames

    def get_user_count(self):
        return 1

    def create_account(self, username):
        '''Trigger the instantiation of a new database and create an account entry in the configuration file.'''

        db_file_name = username + '.db'
        if self.validate_file_name(db_file_name):
            standard_queries.create_db(db_file_name)
            self.db_conn = standard_queries.connect_to_db(db_file_name)
            full_database_path = os.path.join(self.root_path, db_file_name)

            # Instantiate Database
            # self.instantiate_database_schema(db_file_name)
            # self.instantiate_static_tables(db_file_name)
            self.instantiate_dynamic_tables()

            # Create config file entry
            with open(self.config_file_name_path, 'a') as config_file:
                entry_dict = {"username": username, "database": db_file_name,
                              "directory": self.root_path}
                config_file.write(json.dumps(entry_dict) + '\n')
                print('written kitten', entry_dict)
        else:
            # TODO: Return an error
            pass

    def validate_file_name(self, file_name):
        return True

    def instantiate_database_schema(self, league_id, year, week=4):
        # api_params = {'league_id': league_id, 'draft_id': '983048181460119553', 'week': 4} # TODO: pass week as param
        api_params = {'league_id': league_id, 'draft_id': '983048181460119553', 'week': week}
        sleeper_etl.run_sleeper_etl(self.db_conn, api_params, year)

    def instantiate_static_tables(self, db_conn):
        pass

    def instantiate_dynamic_tables(self):
        standard_queries.create_season_table(self.db_conn)


class StartModel():
    def __init__(self, db_conn):
        ...
        self.db_conn = db_conn
        self.visuals = ['Schedule Luck', 'Roster Week Points']
        self.eval_week = self.get_week()

    def get_luck_factor_df(self, week, year):
        df = standard_queries.get_luck_factor_df(self.db_conn, week, year)
        return df

    def get_roster_week_points_df(self, week, year):
        df = standard_queries.get_roster_week_points_df(self.db_conn, week, year)
        return df

    def get_week(self):
        return 4

    def instantiate_database_schema(self, league_id, year, week=4):
        # api_params = {'league_id': league_id, 'draft_id': '983048181460119553', 'week': 4} # TODO: pass week as param
        api_params = {'league_id': league_id, 'draft_id': '983048181460119553', 'week': week}
        sleeper_etl.run_sleeper_etl(self.db_conn, api_params, year)

    def instantiate_static_tables(self, db_conn):
        pass

    def instantiate_dynamic_tables(self, db_conn):
        standard_queries.create_season_table(self.db_conn)


class SeasonModel():
    def __init__(self, db_conn):
        ...
        self.db_conn = db_conn
        self.league_id = None
        self.draft_id = None
        self.year = None

    def get(self, year):
        self.year = year

        season_info = standard_queries.get_season(self.db_conn, year)
        return season_info

    def create(self):
        standard_queries.create_season(self.db_conn, self.year, self.league_id, self.draft_id)

    def get_all(self):
        season_info = standard_queries.get_all_seasons(self.db_conn)
        return season_info

    def load_season_data(self):
        api_params = {'league_id': int(self.league_id), 'draft_id': int(self.draft_id), 'week': 1}
        standard_queries.load_season_data(self.db_conn, api_params, int(self.year))


