import questionary
import re
from rich import print as rprint


class MenuView:

    def __init__(self, manager):
        self.manager = manager

    def main_menu_choices(self) -> list:
        return [
            ]

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

    def display_main_menu(self, role) -> str:
        print('')
        print(50 * '-')

        match role:
            
            case 'M':
                answer = questionary.select(
                    "Que souhaitez-vous faire ?",
                    choices=self.main_menu_choices()
                ).ask()
                return answer
