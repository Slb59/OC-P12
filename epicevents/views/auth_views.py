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
    # username = questionary.text(
    #     "Username:",
    #     validate=lambda text: True if re.match(r"\w", text)
    #     else "Pas de caractère spéciaux"
    # ).ask()
    # regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
    # regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
    # password = questionary.password(
    #     "Password:",
    #     validate=lambda text: True
    #     if re.match(
    #         regex_password,
    #         text)
    #     else "Le format du mot de passe est invalide"
    # ).ask()
    return username, password
