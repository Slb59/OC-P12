import click
from epicevents.controllers.epicmanager import EpicManager
from epicevents.controllers.session import create_session


@click.command()
def mydata():
    """ show data of connected employee"""
    app = EpicManager()
    e = app.check_session()
    if e:
        app.show_profil(e)
        create_session(e, app.env.TOKEN_DELTA, app.env.SECRET_KEY)


@click.command()
def update_mydata():
    """ update data of connected employee """
    app = EpicManager()
    e = app.check_session()
    if e:
        app.update_profil(e)
        create_session(e, app.env.TOKEN_DELTA, app.env.SECRET_KEY)
