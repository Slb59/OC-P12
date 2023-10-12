import click
from epicevents.controllers.epicmanager import EpicManager
from epicevents.controllers.manager_dashboard import EpicManagerDashboard


@click.command()
def login(**kwargs):
    """ login to the database """
    app = EpicManager()
    app.login(**kwargs)


@click.command()
def logout():
    """ logout from database """
    app = EpicManager()
    app.check_logout()


@click.command()
def dashboard():
    """ access to menu """
    controller = EpicManagerDashboard()
    controller.run()


@click.command()
def initbase():
    """ init the database """
    EpicManager.initbase()
