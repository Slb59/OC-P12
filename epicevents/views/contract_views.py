import questionary
import re
from rich.table import Table
from rich import box
from epicevents.views.console import console


class ContractView:

    @classmethod
    def display_list_contracts(cls, all_contracts, pager=True):
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
    def prompt_data_paiement(cls):
        error_text = "Au moins 3 caractères sont requis, alpha ou numérique"
        ref = questionary.text(
            "Référence:",
            validate=lambda text: True
            if re.match(r"^[A-Za-z0-9-]+$", text) and len(text) >= 3
            else error_text).ask()
        if ref is None:
            raise KeyboardInterrupt
        regex_ctrl = r"(?<!-)\b([1-3]?\d{1,5}|100000)\b"
        amount = questionary.text(
            "Montant:",
            validate=lambda text: True
            if re.match(regex_ctrl, text)
            else "Le montant doit être positif et inférieur à 100 000").ask()
        if amount is None:
            raise KeyboardInterrupt
        return {'ref': ref, 'amount': amount}
