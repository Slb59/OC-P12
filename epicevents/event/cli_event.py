import click
from epicevents.controllers.epicmanager import EpicManager
from epicevents.event.manager_event import EpicManagerEvent


@click.group(name='event')
def cli_event():
    """Commands related to events"""
    pass


@cli_event.command()
def list():
    """ list of events """
    app = EpicManager()

    if app.user:
        controle_event = EpicManagerEvent(app.user, app.epic)
        controle_event.list_of_events()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_event.command()
def update():
    """ modify an event """
    app = EpicManager()

    if app.user:
        controle_event = EpicManagerEvent(app.user, app.epic)
        controle_event.update_event()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_event.command()
def create():
    """ create an event """
    app = EpicManager()

    if app.user:
        controle_event = EpicManagerEvent(app.user, app.epic)
        controle_event.create_event()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_event.command()
def close():
    """ close an event """
    app = EpicManager()

    if app.user:
        controle_event = EpicManagerEvent(app.user, app.epic)
        controle_event.terminate_event()
        app.refresh_session()
    app.epic.database_disconnect()


@cli_event.command()
def cancel():
    """ cancel an event """
    app = EpicManager()

    if app.user:
        controle_event = EpicManagerEvent(app.user, app.epic)
        controle_event.cancel_event()
        app.refresh_session()
    app.epic.database_disconnect()


if __name__ == '__main__':
    cli_event()
