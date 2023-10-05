import pandas as pd
import numpy as np
from Load import FantasyApi
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

def roster_week_points(eval_week, roster_week_df, roster_df, user_df):
    # Points by Roster week
    df_1 = (
            roster_week_df
            .drop_duplicates(subset=['roster_id', 'week_id', 'matchup_id'])
            .merge(roster_df, how='left', left_on='roster_id', right_on='roster_id')
            .merge(user_df, how='left', left_on='owner_id', right_on='user_id')
            .loc[lambda df: df.week_id <= eval_week]
            .loc[:, ['display_name', 'roster_id', 'week_id', 'wins', 'losses', 'points']]
            .sort_values(by='week_id', ascending=False)
            )

    df_1['weekly_points_rank'] = (
                                    df_1
                                    .groupby('week_id')
                                    ['points']
                                    .rank(method='min', ascending=False)
                                  )

    roster_week_points_df = df_1.sort_values('points', ascending=False)

    return roster_week_points_df.reset_index()

def roster_week_points_plot(roster_week_points_df, week):
    roster_week_points_df = roster_week_points_df.sort_values('roster_id', ascending=True)
    img_file = r'C:\Users\apuckett\OneDrive - WCF Insurance\Documents\School\FFootball\Vizualizations\Widget Images\crown.png'
    background_image = imageio.v2.imread(img_file, pilmode='RGBA')

    fig, ax = plt.subplots(1, 1)
    fig.patch.set_facecolor(mcolors.CSS4_COLORS['seagreen'])
    fig.patch.set_alpha(0.5)
    ax.set_facecolor(mcolors.CSS4_COLORS['lightgrey'])
    ax.set_alpha(0.2)

    plt.rcParams.update({'font.size': 10, 'font.weight': 'bold', 'font.family': 'DejaVu Sans'})

    # cmap = cm.get_cmap(''Diverging'')
    xtick_spacing = 20
    ind = np.arange(1, 13)*xtick_spacing  # x locations of the rosters
    # width = .35  # The width of the bars
    ax.scatter(roster_week_points_df['roster_id']*xtick_spacing, roster_week_points_df['points'], c=roster_week_points_df['points'], cmap='RdYlGn', vmin=60, vmax=140, marker='o', edgecolor='k', linewidth=.3, s=100)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ylim = [40, roster_week_points_df['points'].max() * 1.05]
    xlim = [0, ax.get_xlim()[1]]
    ax.set_ylabel('Points', fontdict={'fontsize': 13, 'fontweight': 'bold'})
    ax.set_title(f'Week {week} Recap: Weekly Points by Roster', fontdict={'fontsize': 14, 'fontweight': 'bold'})
    ax.set_xticks(ind)
    ax.set_xticklabels(roster_week_points_df['display_name'].unique(), fontdict={'fontsize': 11, 'fontweight': 'bold'})
    plt.xticks(rotation=40, ha='right')
    ax.set_ylim([ylim[0], ylim[1]])
    ax.set_xlim([xlim[0], xlim[1]])
    # ax.legend()
    # ax.text(xlim[1] / 2 - 3.5, ylim[1] * 4 / 5 + .65, 'Schedule Wins (Expected Wins - Actual Wins)')

    # autolabel(ax, rects1, luck_factor_df)
    # autolabel(ax, rects2, luck_factor_df)

    plt.rcParams.update({'font.size': 10, 'font.weight': 'bold', 'font.family': 'DejaVu Sans'})
    ax.grid(axis='y')

    # axin = ax.inset_axes([60, 40, 60+2*(120-105), ylim[0]+2*(120-105)], transform=ax.transData)  # create new inset axes in data coordinates
    king_team = 9 #TODO: Dynamically assign
    king_points = 156.5 #TODO: Dynamically assign
    # king_points = float(roster_week_points_df['points'].max())
    extent = [king_team*20-2, king_team*20+2, king_points+1, king_points+6]
    ax.imshow(background_image, extent=extent)
    # axin.axis('off')
    fig.tight_layout()
    plt.savefig(
        f'C:\\Users\\apuckett\\OneDrive - WCF Insurance\\Documents\\School\\FFootball\\Vizualizations\\Week {week} Point Dist.png',
        facecolor=mcolors.CSS4_COLORS['lightseagreen'])
    plt.show()


if __name__ == '__main__':
    db = 'fantasy.db'
    api = FantasyApi(db)

    league_df = pd.read_sql_query("SELECT * FROM league", api.conn)
    roster_df = pd.read_sql_query("SELECT * FROM roster", api.conn)
    user_df = pd.read_sql_query("SELECT * FROM user", api.conn)
    roster_week_df = pd.read_sql_query("SELECT * FROM roster_week", api.conn)


    eval_week = 4
    roster_week_points_df = roster_week_points(eval_week, roster_week_df, roster_df, user_df)
    roster_week_points_plot(roster_week_points_df, eval_week)
