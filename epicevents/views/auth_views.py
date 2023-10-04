import re
import questionary
from .console import console
from rich.panel import Panel
from rich.text import Text


class AuthView:

    @classmethod
    def display_logout(cls) -> None:
        text = "Vous êtes déconnecté"
        print(text)

    @classmethod
    def display_welcome(cls, username) -> None:
        text = f" Bienvenue {username} sur EpicEvent"
        panel = Panel(Text(text, justify="center"))
        console.print(panel)

    @classmethod
    def display_waiting_databasecreation(cls, f, data):
        with console.status("Création de la base de données ...",
                            spinner="circleQuarters"):
            f(*data)

    @classmethod
    def display_login(cls):
        username = console.input("Identifiant:")
        console.print(username)
        password = console.input("Mot de passe:")
        console.print(password)
        return username, password

    @classmethod
    def prompt_login(cls, **kwargs):
        username = questionary.text(
                "Identifiant:",
                validate=lambda text: True
                if re.match(r"^[a-zA-Z]+$", text)
                else "Seul des caractères alpha sont autorisés",
                **kwargs).ask()
        if username is None:
            raise KeyboardInterrupt
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Password:",
            validate=lambda text: True
            if re.match(regex_password, text)
            else "Le format du mot de passe est invalide", **kwargs).ask()
        if password is None:
            raise KeyboardInterrupt
        return username, password

    @classmethod
    def display_database_connection(cls, name):
        console.print(f'La base {name} est opérationnelle')

    @classmethod
    def prompt_baseinit(cls, **kwargs):
        basename = questionary.text(
                "Nom de votre base de données:",
                validate=lambda text: True
                if re.match(r"^[a-zA-Z]+$", text)
                else "Seul des caractères alpha sont autorisés",
                **kwargs).ask()
        if basename is None:
            raise KeyboardInterrupt
        username = questionary.text(
                "Identifiant administrateur:",
                validate=lambda text: True
                if re.match(r"^[a-zA-Z]+$", text)
                else "Seul des caractères alpha sont autorisés",
                **kwargs).ask()
        if username is None:
            raise KeyboardInterrupt
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Password administrateur:",
            validate=lambda text: True
            if re.match(regex_password, text)
            else "Le format du mot de passe est invalide", **kwargs).ask()
        if password is None:
            raise KeyboardInterrupt  
        port = questionary.text(
                "Port:",
                validate=lambda text: True
                if re.match(r"^[0-9]+$", text)
                else "Seul des chiffres sont autorisés",
                **kwargs).ask()
        if port is None:
            raise KeyboardInterrupt
        return (basename, username, password, port)

    @classmethod
    def prompt_manager(cls, **kwargs):
        username = questionary.text(
                "Identifiant manager:",
                validate=lambda text: True
                if re.match(r"^[a-zA-Z]+$", text)
                else "Seul des caractères alpha sont autorisés",
                **kwargs).ask()
        if username is None:
            raise KeyboardInterrupt
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Password manager:",
            validate=lambda text: True
            if re.match(regex_password, text)
            else "Le format du mot de passe est invalide", **kwargs).ask()
        if password is None:
            raise KeyboardInterrupt
        result = questionary.password(
            "Confirmez le mot de passe:",
            validate=lambda text: True if text == password
            else "Les mots de passe ne correspondent pas",
            **kwargs).ask()
        if result is None:
            raise KeyboardInterrupt
        return (username, password)

    @classmethod
    def prompt_confirm_testdata(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous générer des données de test ?", **kwargs).ask()
