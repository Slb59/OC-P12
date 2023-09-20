import questionary
import re
# from rich import print as rprint


class AuthView:

    def __init__(self, manager):
        self.manager = manager

    def common_lists(self) -> list:
        return [
            "Liste des clients",
            "Liste des contrats",
            "Liste des évènements"
            ]

    def common_choices(self) -> list:
        return [
            "Mes données",
            "Mes tâches",
            "Listes",
            "Déconnexion",
            "Quitter l'application"
            ]

    def manager_choices(self) -> list:
        return self.common_choices() + [
            "Nouvel employé",
            "Modifier le role d'un employé",
            "Modifier le département d'un employé",
            "Invalider la connexion d'un employé",
            "Créer un contrat",
            "Modifier un contrat",
            "Affecter un support à un évènement"
            ]

    def menu_choices(self, role) -> list:
        match role:

            case 'Manager':
                return self.manager_choices()



    def display_menu_manager(self) -> str:
        print(self.manager_choices())
        answer = questionary.select(
                    "Que souhaitez-vous faire ?",
                    choices=self.manager_choices()
                ).ask()
        return answer
