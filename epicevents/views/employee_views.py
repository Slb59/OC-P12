import questionary
import re
from rich.table import Table
from rich import box
from epicevents.views.console import console


class EmployeeView:

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
    def prompt_manager(cls, alls):
        return questionary.select(
            "Choix du manager:",
            choices=alls
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
    def prompt_confirm_profil(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous modifier vos données ?", **kwargs).ask()

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
    def prompt_password(cls, **kwargs):
        regex_password = r"(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])"
        regex_password += "(?=.*?[#?!@$%^&*-]).{8,}"
        password = questionary.password(
            "Mot de passe:",
            validate=lambda text: True
            if re.match(regex_password, text)
            else "Le format du mot de passe est invalide",
            **kwargs).ask()
        if password is None:
            raise KeyboardInterrupt
        result = questionary.password(
            "Confirmez le mot de passe:",
            validate=lambda text: True if text == password
            else "Les mots de passe ne correspondent pas",
            **kwargs).ask()
        if result is None:
            raise KeyboardInterrupt
        return password

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
    def display_list_tasks(cls, all_tasks, pager=True):
        table = Table(title="Mes tâches à réaliser", box=box.SQUARE)
        table.add_column("Id")
        table.add_column("Date demande")
        table.add_column("Description")
        for t in all_tasks:
            str_dates = t.started_time.strftime('%d/%m/%Y')
            table.add_row(str(t.id), str_dates, t.description)
        if pager:
            with console.pager():
                console.print(table)
        else:
            console.print(table)

    @classmethod
    def display_list_employees(
            cls, all_employees, pager=True):

        table = Table(title="Liste des employés", box=box.SQUARE)
        table.add_column("Département")
        table.add_column("Id")
        table.add_column("Identifiant")
        table.add_column("Email")
        table.add_column("Role")
        table.add_column("Statut")

        for e in all_employees:
            table.add_row(
                e.department.name,
                str(e.id), e.username, e.email, e.role.value, e.state.value)

        if pager:
            with console.pager():
                console.print(table)
        else:
            console.print(table)
