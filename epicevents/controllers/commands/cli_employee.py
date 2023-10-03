import click
from epicevents.controllers.epicmanager import EpicManager


@click.group(name='employee')
def cli_employee():
    """Commands related to employees"""
    pass


@cli_employee.command()
def mydata():
    """ show data of connected employee"""
    app = EpicManager()
    app.show_profil()
    app.refresh_session()


@cli_employee.command()
def update_mydata():
    """ update data of connected employee """
    app = EpicManager()    
    app.update_profil()
    app.refresh_session()


@cli_employee.command()
def tasks():
    """ list the tasks of connected employee """
    app = EpicManager()
    app.list_of_task()
    app.refresh_session()


@cli_employee.command()
def terminate_task():
    """ terminate a task """
    app = EpicManager()
    app.terminate_a_task()
    app.refresh_session()


@cli_employee.command()
def list():
    """ list all employees"""
    app = EpicManager()
    app.list_of_employees()
    app.refresh_session()


if __name__ == '__main__':
    app = EpicManager()
    cli_employee(app)
