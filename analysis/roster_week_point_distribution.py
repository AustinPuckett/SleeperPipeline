import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
from matplotlib import cm
import imageio, PIL

def autolabel(ax, rects, luck_factor_df, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """
    plt.rcParams.update({'font.size': 10, 'font.weight': 'normal', 'font.family': 'DejaVu Sans'})
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for i, rect in enumerate(rects):
        height = rect.get_height()
        luck_factor = round(luck_factor_df.iloc[i]['luck_factor'], 1)
        ax.annotate('{}'.format(round(height, 1)),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos] * 3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')






if __name__ == '__main__':
    pass
    # db = 'fantasy.db'
    # api = FantasyApi(db)
    #
    # league_df = pd.read_sql_query("SELECT * FROM league", api.conn)
    # roster_df = pd.read_sql_query("SELECT * FROM roster", api.conn)
    # user_df = pd.read_sql_query("SELECT * FROM user", api.conn)
    # roster_week_df = pd.read_sql_query("SELECT * FROM roster_week", api.conn)
    #
    #
    # eval_week = 4
    # roster_week_points_df = roster_week_points(eval_week, roster_week_df, roster_df, user_df)
    # roster_week_points_plot(roster_week_points_df, eval_week)