from rich.table import Table
from rich import box
from .console import console


def display_list_clients(all_clients):
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
    with console.pager():
        console.print(table)


def display_list_contracts(all_contracts):
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
    with console.pager():
        console.print(table)


def display_list_events(all_events):
    table = Table(title="Liste des contracts", box=box.SQUARE)
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
    with console.pager():
        console.print(table)
