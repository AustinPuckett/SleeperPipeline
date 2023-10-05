import os
from datetime import date
import json
import sqlite3 as sql
import analysis.standard_queries as query

class AccountModel():
    '''TODO: Change working directory once this program is converted to a .exe'''

    def __init__(self):
        self.root_path = os.getcwd()
        self.config_file_name = 'app/config.txt'
        self.config_file_name_path = os.path.join(self.root_path, self.config_file_name)
        self.download_file_path = None
        self.db_conn = None

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
                    self.db_conn = sql.connect(database)
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

    def create_account(self, username, league_id):
        '''Trigger the instantiation of a new database and create an account entry in the configuration file.'''
        db_file_name = username + '.db'
        if self.validate_file_name(db_file_name):
            full_database_path = os.path.join(self.root_path, db_file_name)

            # Instantiate Database
            # self.instantiate_database_schema(db_file_name)
            # self.instantiate_static_tables(db_file_name)
            # self.instantiate_dynamic_tables(db_file_name)

            # Create config file entry
            with open(self.config_file_name_path, 'a') as config_file:
                entry_dict = {"username": username, "database": db_file_name, "league_id": league_id
                              "directory": self.root_path, "draft_ids": {}}
                config_file.write(json.dumps(entry_dict) + '\n')
                print('written kitten', entry_dict)
        else:
            # TODO: Return an error
            pass

    def validate_file_name(self, file_name):
        return True

    def instantiate_database_schema(self, db_name):
        pass

    def instantiate_static_tables(self, db_name):
        pass

    def instantiate_dynamic_tables(self, db_name):
        pass


class StartModel():
    def __init__(self, db_conn):
        ...
        self.db_conn = db_conn
        self.visuals = ['Schedule Luck']

    def get_luck_factor_df(self):
        df = query.luck_factor_df()

    def get_week(self):
        return 4