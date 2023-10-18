import questionary
import re
from rich.table import Table
from rich import box

from epicevents.views.console import console
from epicevents.views.prompt_views import PromptView
from ..views.regexformat import regexformat


class ClientView:

    @classmethod
    def prompt_confirm_client(cls, **kwargs) -> bool:
        """ ask confirm for client selection

        Returns:
            bool: True or False
        """
        return questionary.confirm(
            "Souhaitez-vous sélectionner un client ?", **kwargs).ask()

    @classmethod
    def prompt_client(cls, all_clients, **kwargs) -> str:
        """ask a client full_name in all_clients list

        Args:
            all_clients (_type_): list of full_name

        Returns:
            str: a client full_name
        """
        return PromptView.prompt_select(
                "Choix du client:", all_clients, **kwargs)

    @classmethod
    def prompt_full_name(cls) -> str:
        """ ask to prompt a full_name

        Returns:
            str: the string enter
        """
        return questionary.text(
            "Nom complet:",
            validate=lambda text: True
            if re.match(regexformat['alpha'][0], text)
            else regexformat['alpha'][1]).ask()

    @classmethod
    def prompt_data_client(cls, full_name_required=True) -> dict:
        """ask data information about a client

        Raises:
            KeyboardInterrupt: if ctrl+C enter

        Returns:
            dict: all data enter
        """
        full_name = questionary.text(
            "Nom complet:",
            validate=lambda text: True
            if re.match(regexformat['alpha'][0], text)
            else regexformat['alpha'][1]).ask()
        if full_name_required and full_name is None:
            raise KeyboardInterrupt

        email = questionary.text(
            "Email:",
            validate=lambda text: True
            if re.match(regexformat['email'][0], text)
            else regexformat['email'][1]).ask()

        phone = questionary.text(
            "Phone:",
            validate=lambda text: True
            if re.match(regexformat['phone'][0], text)
            else regexformat['phone'][1]).ask()

        company_name = questionary.text(
            "Entreprise:",
            validate=lambda text: True
            if re.match(regexformat['alpha'][0], text)
            else regexformat['alpha'][1]).ask()
        return {'full_name': full_name, 'email': email, 'phone': phone,
                'company_name': company_name}

    @classmethod
    def display_list_clients(cls, all_clients, pager=True) -> None:
        """ display data of a all_clients list

        Args:
            all_clients (Client list): list of Client instances
            pager (bool, optional): If pager is used. Defaults to True.
        """
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

    @classmethod
    def display_client_info(cls, client) -> None:
        """ display data for a specific client

        Args:
            client (Cleint): a Client instance
        """
        title = f"Données du client {client.full_name}"
        table = Table(title=title, box=box.SQUARE)
        table.add_column("Nom")
        table.add_column("Email")
        table.add_column("Téléphone")
        table.add_column("Entreprise")
        table.add_column("Commercial")
        table.add_column("Nb contrats actifs")
        table.add_column("Nb contrats")
        table.add_row(
                client.full_name, client.email,
                client.phone, client.company_name,
                str(client.commercial), str(len(client.actif_contracts)),
                str(len(client.contracts)),
                )
        console.print(table)
