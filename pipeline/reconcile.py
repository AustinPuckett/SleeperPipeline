import sqlite3 as sql
import pandas as pd
from pipeline.utils import extract_first_two_words, get_item_from_dataframe_list_entry


def reconcile_projections_tables(conn):
    '''Remove suffixes from the "PLAYER NAME" of the projections tables.
     Change team value "JAC" to "JAX".
     Change PLAYER NAME to TEAM where POS = DST
     '''

    cur = conn.cursor()

    for table in ['ros_projections', 'week_projections']:
        query = f'''SELECT * FROM {table}'''
        df = pd.read_sql(query, conn)
        df['PLAYER NAME'] = df['PLAYER NAME'].apply(extract_first_two_words)
        df.loc[df['TEAM'] == 'JAC', 'TEAM'] = 'JAX'
        df.loc[df['position'] == 'DEF', 'PLAYER NAME'] = df[df['position'] == 'DEF']['TEAM']
        df.to_sql(table, conn, if_exists='replace')
        print(df[df['position'] == 'DEF'].iloc[0])
        conn.commit()

        # query = '''SELECT * FROM week_projections'''
        # df = pd.read_sql(query, conn)
        # df['PLAYER NAME'] = df['PLAYER NAME'].apply(extract_first_two_words)
        # df.loc[df['TEAM'] == 'JAC', 'TEAM'] = 'JAX'
        # df.loc[df['position'] == 'DEF', 'PLAYER NAME'] = df[df['position'] == 'DEF']['TEAM']
        # df.to_sql('week_projections', conn, if_exists='replace')
        # conn.commit()

    cur.close()

    return 'Successfully updated the PLAYER NAME and TEAM column in projections tables!'


def reconcile_player_table(conn):
    '''Update position values
    Change full_name to team for fantasy_position = DEF'''

    cur = conn.cursor()

    query = f'''SELECT * FROM player'''
    df = pd.read_sql(query, conn)
    df['full_name'] = df['full_name'].apply(extract_first_two_words)
    df['fantasy_positions'] = df['fantasy_positions'].apply(get_item_from_dataframe_list_entry)

    df.loc[df['fantasy_positions'] == 'DEF', 'full_name'] = df[df['fantasy_positions'] == 'DEF']['team']
    df.to_sql('player', conn, if_exists='replace')
    conn.commit()

    cur.close()

    return 'Successfully updated positions in the player table!'

if __name__ == '__main__':
    db = 'fantasy.db'
    conn = sql.connect(db)
    print(reconcile_projections_tables(conn))
    print(reconcile_player_table(conn))
    conn.close()
