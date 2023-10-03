import click
from epicevents.controllers.epicmanager import EpicManager


@click.group(name='client')
def cli_client():
    """Commands related to clients"""
    pass


@cli_client.command()
def list():
    """ list all the clients """
    app = EpicManager()
    if app.user:
        app.list_of_clients()
        app.refresh_session()


@cli_client.command()
def update_commercial():
    """ modify the commercial of a client """
    app = EpicManager()
    if app.user:
        app.update_client_commercial()
        app.refresh_session()


@cli_client.command()
def create():
    """ create a new client """
    app = EpicManager()
    if app.user:
        app.create_client()
        app.refresh_session()


@cli_client.command()
def update():
    """ modify data of a client """
    app = EpicManager()
    if app.user:
        app.update_client()
        app.refresh_session()


if __name__ == '__main__':
    cli_client()
