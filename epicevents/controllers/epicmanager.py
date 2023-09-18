import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import display_error_login
from epicevents.models.entities import Employee
from .config import Config, Environ
from .database import EpicDatabase
from .session import save_session, load_session, stop_session
from .decorators import is_authenticated


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

    def check_connection(self, username, password) -> Employee:
        return Employee.find_by_userpwd(self.epic.session, username, password)

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
            (username, password) = self.args.login.split('/')
            e = self.check_connection(username, password)
            if e:
                data = e.to_dict()
                data['exp'] = datetime.now(tz=timezone.utc)\
                    + timedelta(seconds=self.env.TOKEN_DELTA)
                print('----------->')
                print(data)
                token = jwt.encode(
                    data, self.env.SECRET_KEY, algorithm='HS256')
                save_session(e.to_dict(), token)

    @is_authenticated
    def check_session(self) -> bool:
        token = load_session()
        user_info = jwt.decode(
                        token, self.env.SECRET_KEY, algorithms=['HS256'])
        username = user_info['username']
        password = user_info['password']
        e = self.check_connection(username, password)
        if e:
            display_welcome(username)
        else:
            display_error_login()
        return True

    @is_authenticated
    def show_menu(self):
        print('------------- show menu -------------')

    def run(self) -> None:

        self.check_logout()
        self.check_login()
        if self.check_session():
            self.show_menu()


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
