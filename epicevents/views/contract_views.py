import questionary
import re
from rich.table import Table
from rich import box
from epicevents.views.console import console
from epicevents.views.prompt_views import PromptView
from .regexformat import regexformat


class ContractView:

    @classmethod
    def select_statut(cls):
        return "Choix du statut:"

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
    def prompt_confirm_close_contract(cls, **kwargs):
        return questionary.confirm(
            "Demander une cloture du contrat ?", **kwargs).ask()

    @classmethod
    def select_contract(cls):
        return "Choix du contrat:"

    @classmethod
    def prompt_select_statut(cls, values):
        PromptView.prompt_select(
                    cls.select_statut(), values)

    @classmethod
    def prompt_select_contract(cls, values):
        PromptView.prompt_select(
                ContractView.select_contract(), values)

    @classmethod
    def prompt_data_contract(cls, **kwargs):
        error_text = regexformat['3cn'][1]
        ref = questionary.text(
            "Référence:",
            validate=lambda text: True
            if re.match(regexformat['3cn'][0], text) and len(text) >= 3
            else error_text, **kwargs).ask()
        if ref is None:
            raise KeyboardInterrupt
        description = questionary.text(
            "Description:",
            validate=lambda text: True
            if re.match(regexformat['alphanum'][0], text)
            else regexformat['alphanum'][1], **kwargs).ask()
        if description is None:
            raise KeyboardInterrupt
        total_amount = questionary.text(
            "Montant:",
            validate=lambda text: True
            if re.match(regexformat['numposmax'][0], text)
            else regexformat['numposmax'][1],
            **kwargs).ask()
        if total_amount is None:
            raise KeyboardInterrupt

        return {'ref': ref, 'description': description,
                'total_amount': total_amount}

    @classmethod
    def prompt_data_paiement(cls, **kwargs):
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
    def workflow_contract_is_over(cls, contract_ref):
        return f"Evénements terminés, solder le contrat {contract_ref}"
