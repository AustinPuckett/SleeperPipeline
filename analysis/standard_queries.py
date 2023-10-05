import sqlite3 as sql
import pandas as pd

def get_roster(conn, roster_id, week, starters_only=False):
    '''Warning: This function uses string formatting of the SQL statement in place of a bind'''

    cursor = conn.cursor()

    query = f'''SELECT r.roster_id, pw.week_id, pw.player_id, pw.starter, pw.matchup_id, p.full_name,
                p.fantasy_positions, p.injury_status, p.team,
                rproj."PROJ. FPTS" as "Ros Proj", wproj."PROJ. FPTS" as "Week Proj"
                FROM roster r
                LEFT JOIN player_week pw ON r.roster_id = pw.roster_id
                LEFT JOIN player p ON pw.player_id = p.player_id
                LEFT JOIN ros_projections rproj ON p.full_name = rproj."PLAYER NAME" AND p.team = rproj.TEAM
                LEFT JOIN week_projections wproj ON p.full_name = wproj."PLAYER NAME" AND p.team = rproj.TEAM AND
                 pw.week_id = wproj.week
                WHERE r.roster_id = {roster_id} AND pw.week_id = {week}
                '''
    roster = pd.read_sql(query, conn)
    # roster = roster.loc[roster['full_name'].isnull(), 'full_name'] = roster['team']
    # roster.loc[roster['full_name'].isnull(), 'full_name'] = roster[roster['full_name'].isnull()]['team']

    # conn.commit()
    cursor.close()

    return roster

def get_player(full_name, pos, team=None):
    pass

def get_roster_df(conn):
    roster_df = pd.read_sql_query("SELECT * FROM roster", conn)
    return roster_df

def get_league_df(conn):
    league_df = pd.read_sql_query("SELECT * FROM league", conn)
    return league_df

def get_user_df(conn):
    user_df = pd.read_sql_query("SELECT * FROM user", conn)
    return user_df

def get_roster_week_df(conn):
    roster_week_df = pd.read_sql_query("SELECT * FROM roster_week", conn)
    return roster_week_df

def get_luck_factor_df(conn, eval_week):
    roster_week_df = pd.read_sql_query("SELECT * FROM roster_week", conn)
    roster_df = pd.read_sql_query("SELECT * FROM roster", conn)
    user_df = pd.read_sql_query("SELECT * FROM user", conn)

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

    df_2 = (
            df_1
            .groupby(['roster_id', 'display_name'])).sum()

    df_2['true_games'] = eval_week * 11
    df_2['true_losses'] = df_2['weekly_points_rank'] - eval_week
    df_2['true_wins'] = df_2['true_games'] - df_2['true_losses']
    df_2['true_win_percentage'] = df_2['true_wins'] / df_2['true_games']
    df_2 = df_2.sort_values('true_win_percentage', ascending=False)
    # df_2.to_html(r'')
    df_2['true_wins'] = df_2['true_wins'] / 11
    df_2['true_losses'] = df_2['true_losses'] / 11
    df_2['wins'] = df_2['wins'] / eval_week
    df_2['losses'] = df_2['losses'] / eval_week
    df_2['luck_factor'] = df_2['wins'] - df_2['true_wins']

    luck_factor_df = df_2.sort_values('luck_factor', ascending=True)

    return luck_factor_df.reset_index()

if __name__ == '__main__':
    db = 'fantasy.db'
    conn = sql.connect(db)

    roster = get_roster(conn, roster_id=7, week=2, starters_only=False)
    # print(roster.head(5))
    # print(roster.iloc[0])
    conn.close()
