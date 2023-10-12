import click
from epicevents.controllers.epicmanager import EpicManager
from epicevents.contract.manager_contract import EpicManagerContract


@click.group(name='contract')
def cli_contract():
    """Commands related to contracts"""
    pass


@cli_contract.command()
def list():
    """ list the contracts """
    app = EpicManager()
    controle_contract = EpicManagerContract(app.user, app.epic)
    if app.user:
        controle_contract.list_of_contracts()
        app.refresh_session()


@cli_contract.command()
def create():
    """ create a contract """
    app = EpicManager()
    controle_contract = EpicManagerContract(app.user, app.epic)
    if app.user:
        controle_contract.create_contract()
        app.refresh_session()


@cli_contract.command()
def update():
    """ modify a contract """
    app = EpicManager()
    controle_contract = EpicManagerContract(app.user, app.epic)
    if app.user:
        controle_contract.update_contract()
        app.refresh_session()


if __name__ == '__main__':
    cli_contract()
