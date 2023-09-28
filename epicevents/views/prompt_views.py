import questionary
import re


class PromptView:

    @classmethod
    def prompt_confirm_commercial(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un commercial ?", **kwargs).ask()

    @classmethod
    def prompt_commercial(cls, all_commercials):
        return questionary.select(
            "Choix du commercial:",
            choices=all_commercials,
        ).ask()

    @classmethod
    def prompt_confirm_client(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un client ?", **kwargs).ask()

    @classmethod
    def prompt_client(cls, all_clients, **kwargs):
        # print(kwargs['input'])
        return questionary.select(
            "Choix du client:",
            choices=all_clients,
            **kwargs
        ).ask()

    @classmethod
    def prompt_confirm_statut(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un statut ?", **kwargs).ask()

    @classmethod
    def prompt_statut(cls, all_states):
        return questionary.select(
            "Choix du statut:",
            choices=all_states,
        ).ask()

    @classmethod
    def prompt_confirm_contract(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un contrat ?", **kwargs).ask()

    @classmethod
    def prompt_contract(cls, all_contracts):
        return questionary.select(
            "Choix du contrat:",
            choices=all_contracts,
        ).ask()

    @classmethod
    def prompt_confirm_support(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un support ?", **kwargs).ask()

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
    def prompt_confirm_task(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous finaliser une tache ?", **kwargs).ask()

    @classmethod
    def prompt_task(cls, all_tasks):
        return questionary.select(
            "Identifiant de la tâche à terminer:",
            choices=all_tasks,
        ).ask()

    @classmethod
    def prompt_confirm_profil(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous modifier vos données ?", **kwargs).ask()

    @classmethod
    def prompt_data_contract(cls):
        error_text = "Au moins 3 caractères sont requis, alpha ou numérique"
        ref = questionary.text(
            "Référence:",
            validate=lambda text: True
            if re.match(r"^[A-Za-z0-9-]+$", text) and len(text) >= 3
            else error_text).ask()
        if ref is None:
            raise KeyboardInterrupt
        description = questionary.text(
            "Description:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z0-9 ]+$", text)
            else "Seul des caractères alpha sont autorisés").ask()
        if description is None:
            raise KeyboardInterrupt
        regex_ctrl = r"(?<!-)\b([1-3]?\d{1,5}|100000)\b"
        total_amount = questionary.text(
            "Montant:",
            validate=lambda text: True
            if re.match(regex_ctrl, text)
            else "Le montant doit être positif et inférieur à 100 000").ask()
        if total_amount is None:
            raise KeyboardInterrupt

        return {'ref': ref, 'description': description,
                'total_amount': total_amount}

    @classmethod
    def prompt_data_profil(cls):
        username = questionary.text(
            "Identifiant:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z]+$", text)
            else "Seul des caractères alpha sont autorisés").ask()
        if username is None:
            raise KeyboardInterrupt
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Password:",
            validate=lambda text: True
            if re.match(regex_password, text)
            else "Le format du mot de passe est invalide").ask()
        if password is None:
            raise KeyboardInterrupt
        regex_email = '^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*'
        regex_email += '@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$'
        result = questionary.password(
            "Confirmez le mot de passe:",
            validate=lambda text: True if text == password
            else "Les mots de passe ne correspondent pas").ask()
        if result is None:
            raise KeyboardInterrupt
        email = questionary.text(
            "Email:",
            validate=lambda text: True if re.match(regex_email, text)
            else "Le format de l'email est invalide").ask()
        if email is None:
            raise KeyboardInterrupt
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
