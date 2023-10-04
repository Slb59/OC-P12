import click
from epicevents.controllers.epicmanager import EpicManager


@click.command()
def login():
    """ login to the database """
    app = EpicManager()
    app.login()


@click.command()
def logout():
    """ logout from database """
    app = EpicManager()
    app.check_logout()


@click.command()
def dashboard():
    """ access to menu """
    app = EpicManager()
    app.run()


@click.command()
def initbase():
    """ init the database """
    EpicManager.initbase()
