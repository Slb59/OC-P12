import jwt

from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import display_error_login
from epicevents.views.menu_views import (
    prompt_choice,
    display_main_menu
)
from epicevents.views.crud_views import display_list_clients
from .config import Config, Environ
from .database import EpicDatabase
from .session import load_session, stop_session, create_session
from .decorators import (
    is_authenticated,
    # is_commercial,
    # is_manager,
    # is_support
)


class EpicManager:

    def __init__(self, args) -> None:

        self.args = args

        # load .env file
        db = Config()
        self.env = Environ()

        # create database
        self.epic = EpicDatabase(**db.db_config)

    def __str__(self) -> str:
        return "CRM EPIC EVENTS"

    def check_logout(self) -> bool:
        """
        Stop the current session
        Returns:
            bool: always return True
        """
        if self.args.logout:
            stop_session()
            display_logout()
        return True

    def check_login(self) -> bool:
        if self.args.login:
            stop_session()
            (username, password) = self.args.login.split('/')
            e = self.epic.check_connection(username, password)
            if e:
                create_session(e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)
            else:
                display_error_login()

    @is_authenticated
    def check_session(self):
        token = load_session()
        user_info = jwt.decode(
                        token, self.env.SECRET_KEY, algorithms=['HS256'])
        username = user_info['username']
        e = self.epic.check_employee(username)
        if e:
            return e
        else:
            display_error_login()
            return None

    @is_authenticated
    def show_menu(self, e):
        # show_mainmenu()
        # print(self.epic.get_clients())
        display_list_clients(self.epic.get_clients())

    def run(self) -> None:

        self.check_logout()
        self.check_login()
        e = self.check_session()
        if e:
            running = True
            try:
                while running:
                    display_welcome(e.username)
                    display_main_menu(e.role.value)
                    prompt_choice()
                    create_session(
                        e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)
            except KeyboardInterrupt:
                pass
