import time
import re
from rich.panel import Panel
from rich.columns import Columns
from rich.align import Align
from rich import box
import questionary
from .console import console, error_console


def thinking():
    time.sleep(30)


def show_waiting(f):
    with console.status("Working...", spinner="circleQuarters"):
        f()


def menu_manager() -> Panel:
    menu_text = "    06-Créer un nouvel employé\n"
    menu_text += "    07-Modifier le role d'un employé\n"
    menu_text += "    08-Modifier le département d'un employé\n"
    menu_text += "    09-Invalider la connexion d'un employé\n"
    menu_text += "    10-Créer un contrat\n"
    menu_text += "    11-Modifier un contrat\n"
    menu_text += "    12-Affecter un support à un évènement"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Menu manager')
    return p


def menu_commercial() -> Panel:
    menu_text = "    06-Créer un nouveau client\n"
    menu_text += "    07-Modifier les données d'un client\n"
    menu_text += "    08-Creer un évènement\n"
    menu_text += "    09-Effectuer une demande de création de contrat\n"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Menu commercial')
    return p


def menu_support() -> Panel:
    menu_text = "    06-Clôturer un évènement\n"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Menu support')
    return p


def menu_role(role) -> Panel:
    match role:
        case "Manager":
            menu = menu_manager()
        case "Commercial":
            menu = menu_commercial()
        case "Support":
            menu = menu_support()
    return menu


def menu_accueil() -> Panel:
    menu_text = "    01-Voir mes données\n"
    menu_text += "    02-Voir mes tâches\n"
    menu_text += "    03-Liste des clients\n"
    menu_text += "    04-Liste des contrats\n"
    menu_text += "    05-Liste des évènements"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Accueil')
    return p


def menu_quit() -> Panel:
    menu_text = "    D-Me déconnecter\n"
    menu_text += "    Q-Quitter l'application"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Quitter')
    return p


def menu_choice(role):

    def ask_prompt():
        return questionary.text(
            "Que voulez-vous faire ?",
            validate=lambda text: True if re.match(r"[0-1][0-9]|D|Q", text)
            else "Votre choix est invalide").ask()

    def check_prompt(result):
        match role:
            case 'Manager': max_menu_idx = 12
            case 'Commercial': max_menu_idx = 9
            case 'Support': max_menu_idx = 6
        if result in ['D', 'Q']:
            return True
        elif int(result) <= max_menu_idx:
            return True
        else:
            return False

    console.print()
    menu = [menu_accueil(), menu_role(role), menu_quit()]
    console.print(Columns(menu))

    result = ask_prompt()
    while not check_prompt(result):
        error_console.print('Votre choix est invalide')
        result = ask_prompt()

    return result