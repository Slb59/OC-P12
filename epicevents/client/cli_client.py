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

    if app.user:
        controle_client = EpicManagerClient(app.user, app.epic)
        controle_client.list_of_clients()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_client.command()
def update_commercial():
    """ modify the commercial of a client """
    app = EpicManager()

    if app.user:
        controle_client = EpicManagerClient(app.user, app.epic)
        controle_client.update_client_commercial()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_client.command()
def create():
    """ create a new client """
    app = EpicManager()

    if app.user:
        controle_client = EpicManagerClient(app.user, app.epic)
        controle_client.create_client()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_client.command()
def update():
    """ modify data of a client """
    app = EpicManager()

    if app.user:
        controle_client = EpicManagerClient(app.user, app.epic)
        controle_client.update_client()
        app.refresh_session()
    app.epic.database_disconnect()


if __name__ == '__main__':
    cli_client()
