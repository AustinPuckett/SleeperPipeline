import pandas as pd
import sqlite3 as sql

def clean_ros_projections(csv_file, player_position):
    df = pd.read_csv(csv_file)
    df['position'] = player_position

    return df

def import_ros_projections(filepaths: dict):
    proj_data = [] #Should be a dataframe!
    for pos, csv_file in  filepaths.items():
        clean_data = clean_ros_projections(csv_file, pos)
        proj_data.append(clean_data)

    return proj_data

def load_ros_projections(db, proj_data, overwrite=True):
    conn = sql.connect(db)
    table_name = 'ros_projections'
    if overwrite:
        fantasy_db.delete_table(conn, table_name)
    for pos_data in proj_data:
        pos_data.to_sql(table_name, conn, if_exists='append')

    return 'Successfully loaded ROS projections!'

def clean_week_projections(csv_file, player_position, week):
    df = pd.read_csv(csv_file)
    df['position'] = player_position
    df['week'] = week

    return df

def import_week_projections(filepaths: dict, week):
    proj_data = [] #Should be a dataframe!
    for pos, csv_file in  filepaths.items():
        clean_data = clean_week_projections(csv_file, pos, week)
        proj_data.append(clean_data)

    return proj_data

def load_week_projections(db, proj_data, overwrite=True):
    conn = sql.connect(db)
    table_name = 'week_projections'
    if overwrite:
        fantasy_db.delete_table(conn, table_name)
    for pos_data in proj_data:
        pos_data.to_sql(table_name, conn, if_exists='append')

    return 'Successfully loaded weekly projections!'

if __name__ == '__main__':
    db = 'fantasy.db'
    week = 2
    filepaths = {'QB': r'',
                'RB': r'',
                'WR': r'',
                'TE': r'',
                'DEF': r'',}

    proj_data = import_ros_projections(filepaths)
    response = load_ros_projections(db ,proj_data)
    print(response)

    filepaths = {'QB': r'',
                'RB': r'',
                'WR': r'',
                'TE': r'',
                'DEF': r'',}

    proj_data = import_week_projections(filepaths, week)
    response = load_week_projections(db, proj_data)
    print(response)
