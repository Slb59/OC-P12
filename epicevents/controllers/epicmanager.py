from epicevents.views.menu import MenuView
from epicevents.models.entities import Employee, NoResultFound
from .config import Config
from .database import EpicDatabase


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

        menuview.display_main_menu(e.role)

        running = True

        while running:
            
            running = False
