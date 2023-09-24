import questionary
import re


class PromptView:

    @classmethod
    def prompt_confirm_commercial(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un commercial ?").ask()

    @classmethod
    def prompt_commercial(cls, all_commercials):
        return questionary.select(
            "Choix du commercial:",
            choices=all_commercials,
        ).ask()

    @classmethod
    def prompt_confirm_client(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un client ?").ask()

    @classmethod
    def prompt_client(cls, all_clients):
        return questionary.select(
            "Choix du client:",
            choices=all_clients,
        ).ask()

    @classmethod
    def prompt_confirm_statut(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un statut ?").ask()

    @classmethod
    def prompt_statut(cls, all_states):
        return questionary.select(
            "Choix du statut:",
            choices=all_states,
        ).ask()

    @classmethod
    def prompt_confirm_contract(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un contrat ?").ask()

    @classmethod
    def prompt_contract(cls, all_contracts):
        return questionary.select(
            "Choix du contrat:",
            choices=all_contracts,
        ).ask()

    @classmethod
    def prompt_confirm_support(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un support ?").ask()

    @classmethod
    def prompt_support(cls, all_supports):
        return questionary.select(
            "Choix du support:",
            choices=all_supports,
        ).ask()

    @classmethod
    def prompt_confirm_task(cls):
        return questionary.confirm(
            "Souhaitez-vous finaliser une tache ?").ask()

    @classmethod
    def prompt_task(cls, all_tasks):
        return questionary.select(
            "Identifiant de la tâche à terminer:",
            choices=all_tasks,
        ).ask()

    @classmethod
    def prompt_confirm_profil(cls):
        return questionary.confirm(
            "Souhaitez-vous modifier vos données ?").ask()

    @classmethod
    def prompt_data_profil(cls):
        username = questionary.text(
            "Identifiant:",
            validate=lambda text: True
            if re.match(r"(?=.*?[a-z])(?=.*?[A-Z])", text)
            else "Seul des caractères alpha sont autorisés").ask()
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Password:",
            validate=lambda text: True
            if re.match(regex_password, text)
            else "Le format du mot de passe est invalide").ask()
        regex_email = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*'
        regex_email += '@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'
        questionary.password(
            "Confirmez votre mot de passe:",
            validate=lambda text: True if text == password
            else "Les mots de passe ne correspondent pas").ask()
        email = questionary.text(
            "Email:",
            validate=lambda text: True if re.match(regex_email, text)
            else "Le format de l'email est invalide").ask()
        return {'username': username, 'password': password, 'email': email}
    
