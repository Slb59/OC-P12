import jwt

from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import display_error_login
from epicevents.views.menu_views import menu_choice
from epicevents.views.list_views import (
    display_list_clients,
    display_list_contracts,
    display_list_events
)
from epicevents.views.prompt_views import (
    prompt_commercial, prompt_confirm_commercial
)
from .config import Config, Environ
from .databasetools import EpicDatabaseWithData
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
        self.epic = EpicDatabaseWithData(**db.db_config)

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
    def list_of_clients(self):
        result = prompt_confirm_commercial()
        if result:
            commercials_name = []
            for c in self.epic.get_commercials():
                commercials_name.append(c.username)
            cname = prompt_commercial(commercials_name)
            display_list_clients(self.epic.get_clients(cname))
        else:
            display_list_clients(self.epic.get_clients())

    @is_authenticated
    def list_of_contracts(self):
        result = prompt_confirm_commercial()
        if result:
            commercials_name = []
            for c in self.epic.get_commercials():
                commercials_name.append(c.username)
            cname = prompt_commercial(commercials_name)
            display_list_contracts(self.epic.get_contracts(cname))
        else:
            display_list_contracts(self.epic.get_contracts())

    @is_authenticated
    def list_of_events(self):
        display_list_events(self.epic.get_events())

    def run(self) -> None:

        self.check_logout()
        self.check_login()
        e = self.check_session()
        if e:
            running = True
            display_welcome(e.username)
            try:
                while running:
                    result = menu_choice(e.role.value)

                    match result:
                        case '03':
                            self.list_of_clients()
                        case '04':
                            self.list_of_contracts()
                        case '05':
                            self.list_of_events()
                        case 'D':
                            stop_session()
                            running = False
                        case 'Q':
                            running = False
                            create_session(
                                e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)

            except KeyboardInterrupt:
                pass
