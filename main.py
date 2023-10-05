if __name__ == '__main__':
    # from pipeline import sleeper_etl

    # sleeper_etl.run_sleeper_etl('fantasy.db', 4, None)
    # print('ok')

    # from analysis.schedule_luck_viz import *
    # from pipeline.load import FantasyApi
    #
    # db = r'C:\Users\pucke\PycharmProjects\SleeperPipeline\fantasy.db'
    # api = FantasyApi(db)
    #
    # conn = api.conn
    #
    # league_df = pd.read_sql_query("SELECT * FROM league", conn)
    # roster_df = pd.read_sql_query("SELECT * FROM roster", conn)
    # user_df = pd.read_sql_query("SELECT * FROM user", conn)
    # roster_week_df = pd.read_sql_query("SELECT * FROM roster_week", conn)
    #
    # conn.close()
    #
    # eval_week = 4
    # luck_factor_df = luck_factor(eval_week, roster_week_df, roster_df, user_df)
    # luck_factor_plot(luck_factor_df, eval_week)

    import app.app_controller as app_controller

    application = app_controller.AppController()
    application.mainloop()
    application.close_connection()

