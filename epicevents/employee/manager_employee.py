from epicevents.controllers.decorators import (
    is_authenticated, is_manager, is_commercial,
    sentry_activate
)
from epicevents.employee.employee_views import EmployeeView
from epicevents.client.client_views import ClientView
from epicevents.views.data_views import DataView


class EpicManagerEmployee():

    def __init__(self, user, base):
        self.user = user
        self.epic = base

    def choice_commercial(self) -> str:
        """
            - ask to confirm a selection
            - read the list in database
            - ask to choose a commercial

        Returns:
            str: commercial username
        """
        # select a commercial
        cname = None
        result = EmployeeView.prompt_confirm_commercial()
        if result:
            commercials = self.epic.dbemployees.get_commercials()
            commercials_name = [c.username for c in commercials]
            cname = EmployeeView.prompt_commercial(commercials_name)
        return cname

    @sentry_activate
    @is_authenticated
    def show_profil(self) -> None:
        """
        read data of the current user and display it
        """
        tasks = self.epic.dbemployees.get_tasks(self.user)
        DataView.display_profil(self.user, len(tasks))

    @sentry_activate
    @is_authenticated
    def update_profil(self):
        """
            - ask confirm to update data
            - show profil data
            - ask new data
            - update database
            - display new data
        """
        result = EmployeeView.prompt_confirm_profil()
        if result:
            tasks = self.epic.dbemployees.get_tasks(self.user)
            DataView.display_profil(self.user, len(tasks))
            profil = EmployeeView.prompt_data_profil(False, False, False)
            self.epic.dbemployees.update_profil(self.user, profil)
            DataView.display_profil(self.user, len(tasks))
            DataView.display_data_update()

    @sentry_activate
    @is_authenticated
    @is_manager
    def list_of_employees(self) -> None:
        """
        read database of employees and display it
        """
        employees = self.epic.dbemployees.get_employees()
        EmployeeView.display_list_employees(employees)

    @sentry_activate
    @is_authenticated
    @is_manager
    def create_new_employee(self) -> None:
        """
            - prompt data of employee
            - update database
        """
        roles = self.epic.dbemployees.get_roles()
        try:
            data = EmployeeView.prompt_data_employee(roles)
            self.epic.dbemployees.create_employee(data)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_employee_role(self) -> None:
        """
            - ask to select an employee
            - ask to select a role
            - update database
        """
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = EmployeeView.prompt_employee(enames)
        roles = self.epic.dbemployees.get_roles()
        role = EmployeeView.prompt_role(roles)
        self.epic.dbemployees.update_employee(
            ename, role=role, manager=self.user)

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_employee_password(self) -> None:
        """
            - ask to select an employee
            - ask the new password
            - update database
        """
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = EmployeeView.prompt_employee(enames)
        password = EmployeeView.prompt_password()
        self.epic.dbemployees.update_employee(ename, password=password)

    @sentry_activate
    @is_authenticated
    @is_manager
    def inactivate_employee(self) -> None:
        """
            - ask to select an employee
            - update database
        """
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = EmployeeView.prompt_employee(enames)
        self.epic.dbemployees.inactivate(ename, self.user)


class EpicManagerTask():

    def __init__(self, user, base):
        self.user = user
        self.epic = base

    @sentry_activate
    @is_authenticated
    def list_of_task(self) -> None:
        """ Read database tasks and display it
        """
        tasks = self.epic.dbemployees.get_tasks(self.user)
        EmployeeView.display_list_tasks(tasks)

    @sentry_activate
    @is_authenticated
    def terminate_a_task(self) -> None:
        """
            - ask to confirm operation
            - ask to select a task
            - update database
        """
        result = EmployeeView.prompt_confirm_task()
        if result:
            all_tasks_id = []
            for t in self.epic.dbemployees.get_tasks(self.user):
                all_tasks_id.append(str(t.id))
            try:
                task = EmployeeView.prompt_select_task(all_tasks_id)
                self.epic.dbemployees.terminate_task(task)
                DataView.display_data_update()
            except KeyboardInterrupt:
                DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_commercial
    def add_task_create_contract(self) -> None:
        """
            - ask to select a manager
            - ask to select a client
            - generate a task to the manager
        """
        managers = self.epic.dbemployees.get_managers()
        managers = [e.username for e in managers]
        manager = EmployeeView.prompt_manager(managers)
        clients = self.epic.dbclients.get_clients(
            commercial_name=self.user.username)
        clients = [c.full_name for c in clients]
        client = ClientView.prompt_client(clients)
        text = 'Creer le contrat du client ' + client
        self.epic.dbemployees.create_task(manager, text)
