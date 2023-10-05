import analysis.schedule_luck_viz as luck_viz
from app.view import *


class LoginPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def login(self, event):
        username = self.view.username_entry.get()
        # password = self.view.bar.get()
        login_response = self.model.validate_login(username)
        if login_response['success'] == True:
            refresh_data = self.view.data_refresh_var.get()
            if refresh_data:
                self.model.instantiate_database_schema(self.model.db_conn, self.model.league_id)
                self.model.instantiate_static_tables(self.model.db_conn)
                self.model.instantiate_dynamic_tables(self.model.db_conn)
            self.master.change_view(StartView)
        else:
            # trigger the view.error method and show the login response
            print(login_response['message'])

    def show_create_account_view(self, event):
        self.master.change_view(CreateAccountView)

    def run(self):
        if self.model.get_user_count() == 0:
            self.master.change_view(CreateAccountView)
        else:
            self.view.init_ui(self)
            self.view.username_entry.config(values=self.model.get_usernames())
            self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class CreateAccountPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view

    def create_account(self, event):
        username = self.view.username_entry.get()
        league_id = self.view.league_id_entry.get()
        self.model.create_account(username, league_id)
        self.master.change_view(LoginView)

    def show_login_view(self, event):
        self.master.change_view(LoginView)

    def run(self):
        self.view.init_ui(self)
        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()


class StartPresenter():
    def __init__(self, master, model, view):
        self.master = master
        self.model = model
        self.view = view
    def render_graph(self, event):
        visual_selection = self.view.visual_selection.get()
        week = self.view.week_selection.get()

        # if (event != None) and (self.view.canvas != None):
        #     self.view.canvas.get_tk_widget().destroy()

        luck_factor_df = self.model.get_luck_factor_df()

        # self.view.canvas = luck_viz.luck_factor_plot(self.view.frame2, luck_factor_df, week)
        # self.view.canvas.get_tk_widget().grid(row=4, column=0, padx=1, pady=3, rowspan=1, columnspan=1)
        luck_viz.luck_factor_plot(luck_factor_df, week)

    def run(self):
        self.view.init_ui(self)

        visuals = self.model.visuals
        if visuals == []:  # TODO: refactor model response as dictionary with a key:value pair to indicate empty result
            pass
        else:
            self.view.visual_selection.config(values=visuals)
            self.view.visual_selection.set(visuals[0])

            self.view.week_selection.config(values=[i for i in range(18)])  # TODO: Dynamically set values
            self.view.week_selection.set(self.model.eval_week)
            # self.render_graph(None)

        self.view.grid()

    def exit_view(self):
        self.view.grid_forget()
