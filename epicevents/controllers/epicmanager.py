import jwt
from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import display_error_login
# from epicevents.models.entities import Employee
from .config import Config, Environ
from .database import EpicDatabase
from .session import load_session, stop_session, create_session
from .decorators import (
    is_authenticated,
    # is_commercial,
    is_manager,
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
            display_welcome(username)
            return e
        else:
            display_error_login()
            return None

    @is_authenticated
    @is_manager
    def show_menu(self, e):
        print('------------- show menu -------------')
        print(e.role.value)

    def run(self) -> None:

        self.check_logout()
        self.check_login()
        e = self.check_session()
        if e:
            self.show_menu(e)

        # # show menu
        # menuview = AuthView(self)
        # if not is_authenticated:
        #     menuview.display_welcome()

        #     (username, password) = menuview.display_login()
        #     e = self.check_connection(username, password)

        #     while e is None:
        #         menuview.display_error_login()
        #         (username, password) = menuview.display_login()
        #         e = self.check_connection(username, password)

        #     data = e.to_dict()
        #     data['exp'] = datetime.now(tz=timezone.utc)\
        #         + timedelta(seconds=self.env.TOKEN_DELTA)
        #     print('----------->')
        #     print(data)
        #     token = jwt.encode(
        #         data, self.env.SECRET_KEY, algorithm='HS256')
        #     save_session(e.to_dict(), token)

        # running = True

        # while running:

        #     match e.role.value:
        #         case "Manager":
        #             answer = menuview.display_menu_manager()
        #             choice = menuview.manager_choices()
        #             index = choice.index(answer)
        #             print('answer ---> ' + answer)
        #             print(index)

        #     running = False
