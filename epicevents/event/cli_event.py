import click
from epicevents.event.manager_event import EpicManagerEvent


@click.group(name='event')
def cli_event():
    """Commands related to events"""
    pass


@cli_event.command()
def list():
    """ list of events """
    app = EpicManagerEvent()
    if app.user:
        app.list_of_events()
        app.refresh_session()


@cli_event.command()
def update():
    """ modify an event """
    app = EpicManagerEvent()
    if app.user:
        app.update_event()
        app.refresh_session()


@cli_event.command()
def create():
    """ create an event """
    app = EpicManagerEvent()
    if app.user:
        app.create_event()
        app.refresh_session()


@cli_event.command()
def close():
    """ close an event """
    app = EpicManagerEvent()
    if app.user:
        app.terminate_event()
        app.refresh_session()


@cli_event.command()
def cancel():
    """ cancel an event """
    app = EpicManagerEvent()
    if app.user:
        app.cancel_event()
        app.refresh_session()


if __name__ == '__main__':
    cli_event()
