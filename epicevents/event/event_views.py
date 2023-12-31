import re
import questionary
from datetime import datetime
from rich.table import Table
from rich import box
from epicevents.views.console import console
from epicevents.views.prompt_views import PromptView
from ..views.regexformat import regexformat


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
    def prompt_data_event(cls, **kwargs):
        title = questionary.text(
            "Titre:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ']+$", text)
            else "Seul des caractères alpha sont autorisés",
            **kwargs).ask()
        if title is None:
            raise KeyboardInterrupt

        description = questionary.text(
            "Description:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ]+$", text)
            else "Seul des caractères alpha sont autorisés",
            **kwargs).ask()

        location = questionary.text(
            "Lieu:",
            validate=lambda text: True
            if re.match(r"^[a-zA-Z ]+$", text)
            else "Seul des caractères alpha sont autorisés",
            **kwargs).ask()

        nb = questionary.text(
            "Nb participants:",
            validate=lambda text: True
            if re.match(r"^[0-9]+$", text)
            and int(text) > 0 and int(text) <= 5000
            else "Nombre compris entre 0 et 5000",
            **kwargs).ask()

        fmt_date = '%d/%m/%Y'
        start = questionary.text(
            "Date de début:",
            validate=lambda text: True
            if re.match(regexformat['date'][0], text)
            else regexformat['date'][1], **kwargs).ask()

        if start:
            end = questionary.text(
                "Date de fin:",
                validate=lambda text: True
                if re.match(regexformat['date'][0], text)
                and datetime.strptime(
                    text, fmt_date) >= datetime.strptime(start, fmt_date)
                else regexformat['date'][1] + " et >= date de début",
                **kwargs).ask()
        else:
            end = None

        return {'title': title, 'description': description,
                'location': location, 'attendees': nb,
                'date_started': start, 'date_ended': end}

    @classmethod
    def select_event(cls):
        return "Choix de l'évènement:"

    @classmethod
    def prompt_select_event(cls, values):
        return PromptView.prompt_select(cls.select_event(), values)

    @classmethod
    def prompt_select_type(cls, values):
        return PromptView.prompt_select(cls.select_type_event(), values)

    @classmethod
    def select_type_event(cls):
        return "Type d'évènement:"

    @classmethod
    def workflow_affect(cls, event_title):
        return f"Vous avez été affecté à l'évènement {event_title}"

    @classmethod
    def workflow_ask_affect(cls, event_title):
        return f"Affecter un support pour l'évènement {event_title}"

    @classmethod
    def no_event(cls):
        return "Il n'y a pas d'évènement sélectionnable"

    @classmethod
    def no_support(cls):
        return "-- sans support --"

    @classmethod
    def prompt_rapport(cls, **kwargs):
        rapport = questionary.text(
            "Votre rapport:",
            validate=lambda text: True
            if re.match(regexformat['alpha'][0], text)
            else regexformat['alpha'][1], **kwargs).ask()
        return rapport
