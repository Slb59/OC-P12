import re
import questionary
from datetime import datetime
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
    def display_no_event(cls):
        console.print("Il n'y a pas d'évènement pour ces critères")

    @classmethod
    def prompt_type(cls, all_types):
        return questionary.select(
            "Type d'évènement:",
            choices=all_types,
        ).ask()

    @classmethod
    def prompt_event(cls, all_events):
        result = questionary.select(
            "Choix de l'évènement:",
            choices=all_events,
        ).ask()
        if result is None:
            raise KeyboardInterrupt
        return result

    @classmethod
    def prompt_data_event(cls):
        title = questionary.text(
            "Titre:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ]+$", text)
            else "Seul des caractères alpha sont autorisés").ask()
        if title is None:
            raise KeyboardInterrupt

        description = questionary.text(
            "Description:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ]+$", text)
            else "Seul des caractères alpha sont autorisés").ask()

        location = questionary.text(
            "Lieu:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ]+$", text)
            else "Seul des caractères alpha sont autorisés").ask()

        nb = questionary.text(
            "Nb participants:",
            validate=lambda text: True
            if re.match(r"^[0-9]+$", text)
            and int(text) > 0 and int(text) <= 5000
            else "Nombre compris entre 0 et 5000").ask()

        regex_date = r'(\d{2})[/.-](\d{2})[/.-](\d{4})$'
        fmt_date = '%d/%m/%Y'
        start = questionary.text(
            "Nb participants:",
            validate=lambda text: True
            if re.match(regex_date, text)
            else "format dd/mm/yyyy attendu").ask()

        if start:
            end = questionary.text(
                "Nb participants:",
                validate=lambda text: True
                if re.match(regex_date, text)
                and datetime.strptime(text, fmt_date) >= start
                else "format dd/mm/yyyy attendu").ask()
        else:
            end = None

        return {'title': title, 'description': description,
                'location': location, 'attendees': nb,
                'date_started': start, 'date_ended': end}

    @classmethod
    def prompt_rapport(cls):
        rapport = questionary.text(
            "Votre rapport:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ']+$", text)
            else "Seul des caractères alpha sont autorisés").ask()
        return rapport
