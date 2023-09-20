import time
from rich.panel import Panel
from rich.prompt import Prompt
from rich.columns import Columns
from rich.align import Align
from rich import box
from .console import console


def thinking():
    time.sleep(30)


def show_waiting(f):
    with console.status("Working...", spinner="circleQuarters"):
        f()


def menu_manager(idx) -> (int, Panel):
    menu_text = f"    {idx+1}-Créer un nouvel employé\n"
    menu_text += f"    {idx+2}-Modifier le role d'un employé\n"
    menu_text += f"    {idx+3}-Modifier le département d'un employé\n"
    menu_text += f"    {idx+4}-Invalider la connexion d'un employé\n"
    menu_text += f"   {idx+5}-Créer un contrat\n"
    menu_text += f"   {idx+6}-Modifier un contrat\n"
    menu_text += f"   {idx+7}-Affecter un support à un évènement"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Menu manager')
    return idx+7, p


def menu_role(idx, role) -> int:
    idx = 5
    match role:
        case "Manager":
            idx, menu = menu_manager(idx)
        case "Commercial":
            ...
        case "Support":
            ...
    return idx, menu


def menu_accueil(idx) -> (int, Panel):
    menu_text = f"    {idx+1}-Voir mes données\n"
    menu_text += f"    {idx+2}-Voir mes tâches\n"
    menu_text += f"    {idx+3}-Liste des clients\n"
    menu_text += f"    {idx+4}-Liste des contrats\n"
    menu_text += f"    {idx+5}-Liste des évènements"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Accueil')
    return idx+5, p


def menu_quit(idx) -> (int, Panel):
    menu_text = f"    {idx+1}-Me déconnecter\n"
    menu_text += f"    {idx+2}-Quitter l'application"
    p = Panel(
        Align.left(menu_text, vertical='top'),
        box=box.ROUNDED,
        title_align='left',
        title='Quitter')
    return idx+2, p


def display_main_menu(role):
    console.print()
    (idx, menu1) = menu_accueil(0)
    (idx, menu2) = menu_role(idx, role)
    (idx, menu3) = menu_quit(idx)
    menu = [menu1, menu2, menu3]
    console.print(Columns(menu))


def prompt_choice():
    Prompt.ask('Que voulez-vous faire ?')
