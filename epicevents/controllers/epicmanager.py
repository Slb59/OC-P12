import jwt
from epicevents.views.menu import MenuView
from epicevents.models.entities import Employee
from .config import Config
from .database import EpicDatabase
from .session import save_session

SECRET_KEY = 'My secret key'


class EpicManager:

    def __init__(self) -> None:
        # load .env file
        db = Config()
        print(db)

        # create database
        self.epic = EpicDatabase(**db.db_config)

    def __str__(self) -> str:
        return "CRM EPIC EVENTS"

    def check_connection(self, username, password) -> Employee:
        return Employee.find_by_userpwd(self.epic.session, username, password)

    def run(self) -> None:

        # show menu
        menuview = MenuView(self)
        menuview.display_welcome()

        (username, password) = menuview.display_login()
        e = self.check_connection(username, password)

        while e is None:
            menuview.display_error_login()
            (username, password) = menuview.display_login()
            e = self.check_connection(username, password)

        token = jwt.encode(e.to_dict(), SECRET_KEY, algorithm='HS256')
        save_session(e.to_dict(), token)
        print(token)
        print(jwt.decode(token, SECRET_KEY, algorithms=['HS256']))

        running = False

        while running:
            
            match e.role.value:
                case "Manager":
                    answer = menuview.display_menu_manager()
                    choice = menuview.manager_choices()
                    index = choice.index(answer)
                    print('answer ---> ' + answer)
                    print(index)                

            running = False
