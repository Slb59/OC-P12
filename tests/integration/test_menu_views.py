import io
from rich.console import Console
from epicevents.views.menu_views import MenuView


def render(panel, width=50) -> str:
    console = Console(file=io.StringIO(), width=width, legacy_windows=False)
    console.print(panel)
    return console.file.getvalue()


def expected_manager():
    expected = "╭─ Menu manager ─────────────────────────────────╮\n"
    expected += "│     06-Liste des employés                      │\n"
    expected += "│     07-Créer un nouvel employé                 │\n"
    expected += "│     08-Modifier le role d'un employé           │\n"
    expected += "│     09-Invalider la connexion d'un employé     │\n"
    expected += "│     10-Créer un contrat                        │\n"
    expected += "│     11-Modifier un contrat                     │\n"
    expected += "│     12-Affecter un commercial à un client      │\n"
    expected += "│     13-Affecter un support à un évènement      │\n"
    expected += "╰────────────────────────────────────────────────╯\n"
    return expected


def expected_commercial():
    expect = "╭─ Menu commercial ────────────────────────────────────────╮\n"
    expect += "│     06-Créer un nouveau client                           │\n"
    expect += "│     07-Modifier les données d'un client                  │\n"
    expect += "│     08-Creer un évènement                                │\n"
    expect += "│     09-Effectuer une demande de création de contrat      │\n"
    expect += "│                                                          │\n"
    expect += "╰──────────────────────────────────────────────────────────╯\n"
    return expect


def expected_support():
    expected = "╭─ Menu support ───────────────────────╮\n"
    expected += "│     06-Clôturer un évènement         │\n"
    expected += "│     07-Annuler un évènement          │\n"
    expected += "│                                      │\n"
    expected += "╰──────────────────────────────────────╯\n"
    return expected


def test_menu_manager():
    expected = expected_manager()
    p = MenuView.menu_manager()
    assert p.title == 'Menu manager'
    assert expected == render(p)


def test_menu_commercial():
    expected = expected_commercial()
    p = MenuView.menu_commercial()
    assert p.title == "Menu commercial"
    assert expected == render(p, 60)


def test_menu_support():
    expected = expected_support()
    p = MenuView.menu_support()
    assert p.title == "Menu support"
    assert expected == render(p, 40)


def test_menu_role():
    p = MenuView.menu_role('M')
    assert render(p) == expected_manager()
    p = MenuView.menu_role('C')
    assert render(p, 60) == expected_commercial()
    p = MenuView.menu_role('S')
    assert render(p, 40) == expected_support()


def test_menu_accueil():
    expected = "╭─ Accueil ──────────────────────────────────────╮\n"
    expected += "│     01-Voir mes données                        │\n"
    expected += "│     02-Voir mes tâches                         │\n"
    expected += "│     03-Liste des clients                       │\n"
    expected += "│     04-Liste des contrats                      │\n"
    expected += "│     05-Liste des évènements                    │\n"
    expected += "╰────────────────────────────────────────────────╯\n"
    p = MenuView.menu_accueil()
    assert p.title == 'Accueil'
    assert render(p) == expected


def test_menu_quit():
    expected = "╭─ Quitter ──────────────────────────────────────╮\n"
    expected += "│     D-Me déconnecter                           │\n"
    expected += "│     Q-Quitter l'application                    │\n"
    expected += "╰────────────────────────────────────────────────╯\n"
    p = MenuView.menu_quit()
    assert p.title == 'Quitter'
    assert render(p) == expected
