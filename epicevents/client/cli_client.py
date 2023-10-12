import click
from epicevents.controllers.epicmanager import EpicManager
from epicevents.client.manager_client import EpicManagerClient


@click.group(name='client')
def cli_client():
    """Commands related to clients"""
    pass


@cli_client.command()
def list():
    """ list all the clients """
    app = EpicManager()
    controle_client = EpicManagerClient(app.user, app.epic)
    if app.user:
        controle_client.list_of_clients()
        app.refresh_session()


@cli_client.command()
def update_commercial():
    """ modify the commercial of a client """
    app = EpicManager()
    controle_client = EpicManagerClient(app.user, app.epic)
    if app.user:
        controle_client.update_client_commercial()
        app.refresh_session()


@cli_client.command()
def create():
    """ create a new client """
    app = EpicManager()
    controle_client = EpicManagerClient(app.user, app.epic)
    if app.user:
        controle_client.create_client()
        app.refresh_session()


@cli_client.command()
def update():
    """ modify data of a client """
    app = EpicManager()
    controle_client = EpicManagerClient(app.user, app.epic)
    if app.user:
        controle_client.update_client()
        app.refresh_session()


if __name__ == '__main__':
    cli_client()
