import pandas as pd
import numpy as np
from pipeline.load import FantasyApi
from matplotlib import pyplot as plt
from matplotlib.patches import Circle
import matplotlib.colors as mcolors
# import matplotlib
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

def luck_factor_plot(luck_factor_df, week):
    # matplotlib.use('TKAgg')
    luck_factor_df = luck_factor_df.sort_values('wins', ascending=False)
    img_file = r'C:\Users\pucke\PycharmProjects\SleeperPipeline\images\football_field.jpg'
    background_image = imageio.v2.imread(img_file, pilmode='RGBA')

    fig, ax = plt.subplots(1, 1)
    fig.patch.set_facecolor(mcolors.CSS4_COLORS['mediumseagreen'])
    fig.patch.set_alpha(0.4)

    plt.rcParams.update({'font.size': 10, 'font.weight': 'bold', 'font.family': 'DejaVu Sans'})

    ind = np.arange(12)  # x locations of the rosters
    width = .35  # The width of the bars

    rects1 = ax.bar(ind - width / 2, luck_factor_df['wins'], width, label='Wins', color=mcolors.CSS4_COLORS['gold'],
                    edgecolor=mcolors.CSS4_COLORS['dimgrey'])
    rects2 = ax.bar(ind + width / 2, luck_factor_df['true_wins'], width, label='Expected Wins',
                    color=mcolors.CSS4_COLORS['lightgrey'], edgecolor=mcolors.CSS4_COLORS['black'])

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ylim = [0, max(luck_factor_df['wins'].max() * 1.5, 5)]
    xlim = [0, ax.get_xlim()[1]]
    ax.set_ylabel('Wins', fontdict={'fontsize': 13, 'fontweight': 'bold'})
    ax.set_title(f'Week {week} Recap: Schedule Luck by Roster', fontdict={'fontsize': 14, 'fontweight': 'bold'})
    ax.set_xticks(ind)
    ax.set_xticklabels(luck_factor_df['display_name'], fontdict={'fontsize': 11, 'fontweight': 'bold'})
    plt.xticks(rotation=40, ha='right')
    ax.set_ylim([ylim[0], ylim[1]])
    ax.legend()
    ax.text(xlim[1] / 2 - 2, ylim[1] * 4 / 5 + .65, 'Schedule Wins (Expected Wins - Actual Wins)')

    autolabel(ax, rects1, luck_factor_df)
    autolabel(ax, rects2, luck_factor_df)

    plt.rcParams.update({'font.size': 10, 'font.weight': 'bold', 'font.family': 'DejaVu Sans'})
    # Luck Index and circle plots
    max_luck = luck_factor_df['luck_factor'].max()
    for i, rect in enumerate(rects1):
        luck_factor = round(luck_factor_df.iloc[i]['luck_factor'], 1)
        height = rect.get_height()
        circle_color = (0.45 - (luck_factor / max_luck) * .20, 0.45 + (luck_factor / max_luck) * .20, 0.1, 0.3)
        circ = Circle((rect.get_x() + rect.get_width(), ylim[1] * 4 / 5 + .2), radius=.35, fill=True, edgecolor='k',
                      facecolor=circle_color, linewidth=1.2)
        plt.gca().add_patch(circ)
        ax.annotate('{}'.format(luck_factor),
                    xy=(rect.get_x() + rect.get_width(), ylim[1] * 4 / 5 + .2),
                    xytext=(0, -5),  # use 0 points offset
                    textcoords="offset points",  # in both directions
                    ha='center', va='bottom')

    fig.tight_layout()
    ax.imshow(background_image, extent=[ax.get_xlim()[0], xlim[1], ylim[0], ylim[1]])
    plt.savefig(
        f'fig.jpeg',
        facecolor=mcolors.CSS4_COLORS['lightseagreen'])
    plt.show()


if __name__ == '__main__':
    db = r'C:\Users\pucke\PycharmProjects\SleeperPipeline\fantasy.db'
    api = FantasyApi(db)

    conn = api.conn

    league_df = pd.read_sql_query("SELECT * FROM league", conn)
    roster_df = pd.read_sql_query("SELECT * FROM roster", conn)
    user_df = pd.read_sql_query("SELECT * FROM user", conn)
    roster_week_df = pd.read_sql_query("SELECT * FROM roster_week", conn)

    conn.close()

    eval_week = 4
    luck_factor_df = luck_factor(eval_week, roster_week_df, roster_df, user_df)
    luck_factor_plot(luck_factor_df, eval_week)
