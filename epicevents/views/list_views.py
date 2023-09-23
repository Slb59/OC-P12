from rich.table import Table
from rich import box
from epicevents.views.console import console


class DisplayView:

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
