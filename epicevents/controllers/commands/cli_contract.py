import click
from epicevents.controllers.epicmanager import EpicManager


@click.group(name='contract')
def cli_contract():
    """Commands related to contracts"""
    pass


@cli_contract.command()
def list():
    """ list the contracts """
    app = EpicManager()
    if app.user:
        app.list_of_contracts()
        app.refresh_session()


@cli_contract.command()
def create():
    """ create a contract """
    app = EpicManager()
    if app.user:
        app.create_contract()
        app.refresh_session()


@cli_contract.command()
def update():
    """ modify a contract """
    app = EpicManager()
    if app.user:
        app.update_contract()
        app.refresh_session()


if __name__ == '__main__':
    cli_contract()
