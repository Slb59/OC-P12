import questionary
from rich.table import Table
from rich import box
from epicevents.views.console import console


class EventView:

    @classmethod
    def display_list_events(cls, all_events, pager=True):
        table = Table(title="Liste des évènements", box=box.SQUARE)
        table.add_column("Client")
        table.add_column("Ref. Contrat")
        table.add_column("Type")
        table.add_column("Titre")
        table.add_column("Lieu")
        table.add_column("Nb. participants")
        table.add_column("Dates")
        table.add_column("Statut")
        table.add_column("Commercial")
        table.add_column("Support")

        for e in all_events:
            if e.support:
                str_support = e.support.username
            else:
                str_support = ''
            fmt_date = '%d/%m/%Y-%Hh%M'
            str_dates = f'du {e.date_started.strftime(fmt_date)}'
            str_dates += f'\nau {e.date_ended.strftime(fmt_date)}'
            table.add_row(
                e.contract.client.full_name,
                e.contract.ref,
                e.type.title, e.title,
                e.location, str(e.attendees),
                str_dates, e.state.value,
                e.contract.client.commercial.username,
                str_support
                )
        if pager:
            with console.pager():
                console.print(table)
        else:
            console.print(table)

    @classmethod
    def prompt_event(cls, all_events):
        return questionary.select(
            "Choix de l'évènement:",
            choices=all_events,
        ).ask()
