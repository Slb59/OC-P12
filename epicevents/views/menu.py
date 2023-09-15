import questionary
import re
from rich import print as rprint


class MenuView:

    def __init__(self, manager):
        self.manager = manager

    def common_choices(self) -> list:
        return [
            "My profile",
            "My tasks",
            "List of employees",
            "List of clients",
            "List of contracts",
            "Liste of events",
            "Logout",
            "Exit"
            ]

    def manager_choices(self) -> list:
        return self.common_choices() + [
            "Add new employee",
            "Update employee role",
            "Update employee department",
            "Invalidate an employee connection",
            "Create a contract",
            "Modify a contract",
            "Affecte support on event"
            ]

    def menu_choices(self, role) -> list:
        match role:

            case 'Manager':
                return self.manager_choices()

    def display_welcome(self) -> None:
        text = " Welcome in EpicEvent manager "
        print(len(text) * '-')
        print(text)
        print(len(text) * '-')
        print('')

    def display_login(self) -> str:
        username = questionary.text(
            "Username:",
            validate=lambda text: True if re.match(r"\w", text)
            else "No special characters please"
        ).ask()
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Password:",
            validate=lambda text: True
            if re.match(
                regex_password,
                text)
            else "The password format is invalid"
        ).ask()
        return username, password

    def display_error_login(self):
        rprint('[bold red]ERROR : password or user not defined')

    def display_menu_manager(self) -> str:
        print(self.manager_choices())
        answer = questionary.select(
                    "Que souhaitez-vous faire ?",
                    choices=self.manager_choices()
                ).ask()
        return answer
