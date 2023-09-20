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
        table.add_row(c.full_name, c.email, c.phone, c.company_name)
    console.print(table)
