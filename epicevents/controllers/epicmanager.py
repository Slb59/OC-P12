import jwt

from epicevents.views.auth_views import AuthView
from epicevents.views.error import ErrorView

from .config import Config, Environ, create_config
from .databasetools import EpicDatabase, EpicDatabaseWithData
from .session import load_session, stop_session, create_session
from .decorators import (is_authenticated, sentry_activate)


class EpicManager:

    def __init__(self) -> None:

        # load .env file
        self.env = Environ()

        # create database
        db = self.get_config()
        self.epic = EpicDatabase(**db.db_config)

        # lit la session courante
        self.user = self.check_session()

    def __str__(self) -> str:
        return "CRM EPIC EVENTS"

    def get_config(self):
        fichier_ini = self.env.DEFAULT_DATABASE + "_database.ini"
        return Config(fichier_ini)

    @is_authenticated
    def check_logout(self) -> bool:
        """
        Stop the current session
        Returns:
            bool: always return True
        """
        stop_session()
        AuthView.display_logout()
        return True

    @sentry_activate
    def login(self, **kwargs) -> bool:
        stop_session()
        (username, password) = AuthView.prompt_login(**kwargs)
        e = self.epic.check_connection(username, password)
        if e:
            create_session(e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)
            return True
        else:
            ErrorView.display_error_login()
            return False

    @sentry_activate
    def check_session(self):
        token = load_session()
        if token:
            user_info = jwt.decode(
                            token, self.env.SECRET_KEY, algorithms=['HS256'])
            username = user_info['username']
            e = self.epic.check_employee(username)
            if e:
                return e

    def refresh_session(self):
        create_session(self.user, self.env.TOKEN_DELTA, self.env.SECRET_KEY)

    @classmethod
    def initbase(cls):
        stop_session()
        values = AuthView.prompt_baseinit()

        file = create_config(*values)
        db = Config(file)
        result = AuthView.prompt_confirm_testdata()
        if result:
            EpicDatabaseWithData(**db.db_config)
        else:
            EpicDatabase(**db.db_config)
        AuthView.display_database_connection(values[0])
