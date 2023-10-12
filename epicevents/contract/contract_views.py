import questionary
import re
from rich.table import Table
from rich import box
from epicevents.views.console import console
from epicevents.views.prompt_views import PromptView
from ..views.regexformat import regexformat


class ContractView:

    @classmethod
    def display_list_contracts(cls, all_contracts, pager=True) -> None:
        """ Display the list of contracts

        Args:
            all_contracts (list): list of instance of Contract
            pager (bool, optional): If pager is used. Defaults to True.
        """
        table = Table(title="Liste des contracts", box=box.SQUARE)
        table.add_column("Référence")
        table.add_column("Client")
        table.add_column("Montant")
        table.add_column("Reste dû")
        table.add_column("Statut")
        table.add_column("Nb évènements")
        table.add_column("Commercial")
        for c in all_contracts:
            table.add_row(
                c.ref, c.client.full_name,
                str(c.total_amount), str(c.outstanding),
                c.state.value, str(len(c.events)),
                c.client.commercial.username
            )
        if pager:
            with console.pager():
                console.print(table)
        else:
            console.print(table)

    @classmethod
    def display_contract_info(cls, contract) -> None:
        """ display data for a specific contract

        Args:
            client (Contract): a Contract instance
        """
        title = f"Données du contract {contract.ref}"
        table = Table(title=title, box=box.SQUARE)
        table.add_column("Référence")
        table.add_column("Description")
        table.add_column("Client")
        table.add_column("Montant")
        table.add_column("Reste dû")
        table.add_column("Statut")
        table.add_column("Nb évènements")
        table.add_column("Commercial")
        table.add_row(
                contract.ref, contract.description, contract.client.full_name,
                str(contract.total_amount), str(contract.outstanding),
                contract.state.value, str(len(contract.events)),
                contract.client.commercial.username
                )
        console.print(table)

    @classmethod
    def prompt_confirm_contract(cls, **kwargs) -> bool:
        """ ask if a contract have to be selected

        Returns:
            bool: True or False
        """
        return questionary.confirm(
            "Souhaitez-vous sélectionner un contrat ?", **kwargs).ask()

    @classmethod
    def prompt_confirm_close_contract(cls, **kwargs) -> bool:
        """ ask if a contract have to be closed

        Returns:
            bool: True or False
        """
        return questionary.confirm(
            "Demander une cloture du contrat ?", **kwargs).ask()

    @classmethod
    def prompt_select_statut(cls, values) -> str:
        """ propose to select a statut in the list of values

        Args:
            values (list): list of states name

        Returns:
            str: the name of state selected
        """
        return PromptView.prompt_select(
                    "Choix du statut:", values)

    @classmethod
    def prompt_select_contract(cls, values):
        """ propose to select a contract in the list of values

        Args:
            values (list): list of Contract.ref

        Returns:
            str: the Contract.ref selected
        """
        return PromptView.prompt_select(
                "Choix du contrat:", values)

    @classmethod
    def prompt_data_contract(cls,
                             ref_required=True,
                             mt_required=True, **kwargs) -> dict:
        """ ask all data of a contract

        Raises:
            KeyboardInterrupt: if ctrl+C is enter

        Returns:
            dict: example:
            {'ref': ref, 'description': description,
                'total_amount': total_amount}
        """
        error_text = regexformat['3cn'][1]
        ref = questionary.text(
            "Référence:",
            validate=lambda text: True
            if re.match(regexformat['3cn'][0], text) and len(text) >= 3
            else error_text, **kwargs).ask()
        if ref_required and ref is None:
            raise KeyboardInterrupt

        description = questionary.text(
            "Description:",
            validate=lambda text: True
            if re.match(regexformat['alphanum'][0], text)
            else regexformat['alphanum'][1], **kwargs).ask()

        total_amount = questionary.text(
            "Montant:",
            validate=lambda text: True
            if re.match(regexformat['numposmax'][0], text)
            else regexformat['numposmax'][1],
            **kwargs).ask()
        if mt_required and total_amount is None:
            raise KeyboardInterrupt

        return {'ref': ref, 'description': description,
                'total_amount': total_amount}

    @classmethod
    def prompt_data_paiement(cls, **kwargs) -> dict:
        """ ask for data of a paiement

        Raises:
            KeyboardInterrupt: if ctrl+C is enter

        Returns:
            dict: example
            {'ref': ref, 'amount': amount}
        """
        ref = questionary.text(
            "Référence:",
            validate=lambda text: True
            if re.match(regexformat['3cn'][0], text) and len(text) >= 3
            else regexformat['3cn'][1], **kwargs).ask()
        if ref is None:
            raise KeyboardInterrupt
        amount = questionary.text(
            "Montant:",
            validate=lambda text: True
            if re.match(regexformat['numposmax'][0], text)
            else regexformat['numposmax'][1],
            **kwargs).ask()
        if amount is None:
            raise KeyboardInterrupt
        return {'ref': ref, 'amount': amount}

    @classmethod
    def workflow_contract_is_over(cls, contract_ref) -> str:
        """ return format string to say a contract need to be sold

        Args:
            contract_ref (str): ref of the Contract

        Returns:
            str: the format string
        """
        return f"Evénements terminés, solder le contrat {contract_ref}"
