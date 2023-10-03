import click
from epicevents.controllers.epicmanager import EpicManager


@click.command()
@click.option('--id', prompt='Identifiant', help='Votre identifiant')
@click.option('--password', prompt='Mot de passe', help='Votre mot de passe')
def login(id, password):
    """ login to the database """
    app = EpicManager()
    app.check_login(id, password)


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
