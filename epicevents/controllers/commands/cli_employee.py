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
    if app.user:
        app.show_profil()
        app.refresh_session()


@cli_employee.command()
def update_mydata():
    """ update data of connected employee """
    app = EpicManager()
    if app.user:
        app.update_profil()
        app.refresh_session()


@cli_employee.command()
def tasks():
    """ list the tasks of connected employee """
    app = EpicManager()
    if app.user:
        app.list_of_task()
        app.refresh_session()


@cli_employee.command()
def terminate_task():
    """ terminate a task """
    app = EpicManager()
    if app.user:
        app.terminate_a_task()
        app.refresh_session()


@cli_employee.command()
def list():
    """ list all employees"""
    app = EpicManager()
    if app.user:
        app.list_of_employees()
        app.refresh_session()


@cli_employee.command()
def create():
    """ create a new employee """
    app = EpicManager()
    if app.user:
        app.create_new_employee()
        app.refresh_session()


@cli_employee.command()
def update_role():
    """ modify the role of an employee """
    app = EpicManager()
    if app.user:
        app.update_employee_role()
        app.refresh_session()


@cli_employee.command()
def update_password():
    """ modify the password of an employee """
    app = EpicManager()
    if app.user:
        app.update_employee_password()
        app.refresh_session()


@cli_employee.command()
def inactivate():
    """ inactivate an employee """
    app = EpicManager()
    if app.user:
        app.inactivate_employee()
        app.refresh_session()


@cli_employee.command()
def task_contract():
    """ ask a manager for creating a contract """
    app = EpicManager()
    if app.user:
        app.add_task_create_contract()
        app.refresh_session()


if __name__ == '__main__':
    cli_employee()
