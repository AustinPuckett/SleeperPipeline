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

if __name__ == '__main__':
    db = 'fantasy.db'
    conn = sql.connect(db)

    roster = get_roster(conn, roster_id=7, week=2, starters_only=False)
    # print(roster.head(5))
    # print(roster.iloc[0])
    conn.close()
