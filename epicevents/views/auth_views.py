import re
import questionary
from .console import console
from rich.panel import Panel
from rich.text import Text


def display_logout() -> None:
    text = "Vous êtes déconnecté"
    print(text)


def display_welcome(username) -> None:
    text = f" Bienvenue {username} sur EpicEvent"
    panel = Panel(Text(text, justify="center"))
    console.print(panel)


def display_waiting_databasecreation(f):
    with console.status("Création de la base de données ...",
                        spinner="circleQuarters"):
        f()


def display_login():
    username = console.input("Identifiant:")
    console.print(username)
    password = console.input("Mot de passe:")
    console.print(password)
    return username, password


def prompt_login(**kwargs):
    username = questionary.text(
            "Identifiant:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z]+$", text)
            else "Seul des caractères alpha sont autorisés", **kwargs).ask()
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


def display_database_connection(name):
    console.print(f'Vous êtes connecté à la base {name}')
