import questionary
import re
from rich.table import Table
from rich import box
from epicevents.views.console import console


class ClientView:

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

    @classmethod
    def display_list_clients(cls, all_clients, pager=True):
        table = Table(title="Liste des clients", box=box.SQUARE)
        table.add_column("Nom")
        table.add_column("Email")
        table.add_column("Téléphone")
        table.add_column("Entreprise")
        table.add_column("Commercial")
        table.add_column("Nb contrats actifs")
        table.add_column("Nb contrats")
        for c in all_clients:
            table.add_row(
                c.full_name, c.email, c.phone, c.company_name,
                str(c.commercial), str(len(c.actif_contracts)),
                str(len(c.contracts)),
                )
        if pager:
            with console.pager():
                console.print(table)
        else:
            console.print(table)
