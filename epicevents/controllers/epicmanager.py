import jwt
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from epicevents.views.menu import MenuView
from epicevents.models.entities import Employee
from .config import Config, Environ
from .database import EpicDatabase
from .session import save_session, load_session


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

    def run(self) -> None:

        if not self.args.login:

            # try token connection
            token = load_session()
            if token is None:
                is_authenticated = False
            else:
                try:
                    decoded_token = jwt.decode(
                        token, self.env.SECRET_KEY, algorithms=['HS256'])

                    username = decoded_token['username']
                    password = decoded_token['password']
                    e = self.check_connection(username, password)
                except InvalidSignatureError as error:
                    print(f'{error}')
                    e = None
                except ExpiredSignatureError as error:
                    print(f'{error}')
                    e = None
                is_authenticated = (e is not None)

        else:
            (username, password) = self.args.login.split('/')
            e = self.check_connection(username, password)
            is_authenticated = (e is not None)

        # show menu
        menuview = MenuView(self)
        if not is_authenticated:
            menuview.display_welcome()

            (username, password) = menuview.display_login()
            e = self.check_connection(username, password)

            while e is None:
                menuview.display_error_login()
                (username, password) = menuview.display_login()
                e = self.check_connection(username, password)

            data = e.to_dict()
            data['exp'] = datetime.now(tz=timezone.utc) + timedelta(seconds=self.env.TOKEN_DELTA)
            print('----------->')
            print(data)
            token = jwt.encode(
                data, self.env.SECRET_KEY, algorithm='HS256')
            save_session(e.to_dict(), token)

        running = True

        while running:

            match e.role.value:
                case "Manager":
                    answer = menuview.display_menu_manager()
                    choice = menuview.manager_choices()
                    index = choice.index(answer)
                    print('answer ---> ' + answer)
                    print(index)                

            running = False
