import pandas as pd
import numpy as np
from standard_queries import get_roster, get_player
# from utils import roster_transaction
import sqlite3 as sql

def calculate_roster_fpts(roster):
    # roster['starter Ros Proj'] = roster['Ros Proj'] * roster['starter']
    # roster['starter Week Proj'] = roster['Week Proj'] * roster['starter']
    # roster.loc[roster['starter Ros Proj'] == '', 'starter Ros Proj'] = 0
    ros_fpts = roster[roster['starter'] == 1]['Ros Proj'].astype(float).sum()
    # roster.loc[roster['starter Week Proj'] == '', 'starter Week Proj'] = 0
    # week_fpts = roster['starter Week Proj'].sum()
    week_fpts = roster[roster['starter'] == 1]['Week Proj'].astype(float).sum()
    # print(np.sum(np.multiply(roster['Ros Proj'], roster['starter']).astype(float)))
    # week_fpts = np.sum(np.multiply(roster['Week Proj'], roster['starter']))

    fpts = {}
    fpts['Ros Proj'] = ros_fpts
    fpts['Week Proj'] = week_fpts
    # print(fpts)
    return fpts

def optimize_roster_pts(roster):

    return roster

def roster_evaluation(roster):
    roster_eval={}
    roster_eval['Ros Proj'] = calculate_roster_fpts(roster)['Ros Proj']
    roster_eval['Week Proj'] = calculate_roster_fpts(roster)['Week Proj']

    return roster_eval


def roster_transaction(roster, add: list, drop: list):
    pass

def trade_evaluator(roster1, roster2, roster1_players, roster2_players):
    roster1 = optimize_roster_pts(roster1)
    roster2 = optimize_roster_pts(roster2)

    roster1_new = roster_transaction(roster1, add=roster2_players, drop=roster1_players)
    roster2_new = roster_transaction(roster2, add=roster1_players, drop=roster2_players)
    roster1_new = optimize_roster_pts(roster1_new)
    roster2_new = optimize_roster_pts(roster2_new)
    
    roster1_eval = roster_evaluation(roster1)
    roster2_eval = roster_evaluation(roster2)
    roster1_new_eval = roster_evaluation(roster1_new)
    roster2_new_eval = roster_evaluation(roster2_new)
    
    roster1_gain = roster1_new_eval['optimized projected points per week'] - roster1_eval['optimized projected points per week']
    roster2_gain = roster2_new_eval['optimized projected points per week'] - roster2_eval['optimized projected points per week']
    trade_eval = {'Roster 1 Gain': roster1_gain, 'Roster 2 Gain': roster2_gain}

    return trade_eval


if __name__ == '__main__':
    # roster1 = get_roster(1)
    # roster2 = get_roster(2)
    # roster1_players = [get_player('Full Name', 'POS', team='team')]
    # roster2_players = [get_player('Full Name', 'POS', team='team')]
    #
    # trade_eval = trade_evaluator(roster1, roster2, roster1_players, roster2_players)
    db = 'fantasy.db'
    conn = sql.connect(db)

    i=5
    week=2

    for i in range(1, 13):
        roster1 = get_roster(conn, i,week=week)
        print(f'roster{i} ', roster_evaluation(roster1))
    # roster_evaluation(roster1)

    conn.close()
