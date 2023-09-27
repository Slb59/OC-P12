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
            choices=all_supports
        ).ask()

    @classmethod
    def prompt_employee(cls, all_employees):
        return questionary.select(
            "Sélectionnez un employé:",
            choices=all_employees
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
            "Confirmez le mot de passe:",
            validate=lambda text: True if text == password
            else "Les mots de passe ne correspondent pas").ask()
        email = questionary.text(
            "Email:",
            validate=lambda text: True if re.match(regex_email, text)
            else "Le format de l'email est invalide").ask()
        return {'username': username, 'password': password, 'email': email}

    @classmethod
    def prompt_role(cls, all_roles):
        role = questionary.select(
            "Role:",
            choices=all_roles,
        ).ask()
        return role

    @classmethod
    def prompt_data_employee(cls, all_roles):
        data = cls.prompt_data_profil()
        data['role'] = cls.prompt_role(all_roles)
        return data

    @classmethod
    def prompt_data_client(cls):
        full_name = questionary.text(
            "Nom complet:",
            validate=lambda text: True
            if re.match(r"(?=.*?[a-z])(?=.*?[A-Z])", text)
            else "Seul des caractères alpha sont autorisés").ask()
        regex_email = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*'
        regex_email += '@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'
        email = questionary.text(
            "Email:",
            validate=lambda text: True if re.match(regex_email, text)
            else "Le format de l'email est invalide").ask()
        regex_phone = "/\\(?([0-9]{3})\\)?([ .-]?)([0-9]{3})\2([0-9]{4})/"
        phone = questionary.text(
            "Phone:",
            validate=lambda text: True if re.match(regex_phone, text)
            else "Ce n'est pas un numéro de téléphone valide").ask()
        company_name = questionary.text(
            "Entreprise:",
            validate=lambda text: True
            if re.match(r"(?=.*?[a-z])(?=.*?[A-Z])", text)
            else "Seul des caractères alpha sont autorisés").ask()
        return {'full_name': full_name, 'email': email, 'phone': phone,
                'company_name': company_name}
