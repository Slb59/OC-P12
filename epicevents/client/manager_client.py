import random
from epicevents.controllers.decorators import (
    is_authenticated, is_manager, is_commercial,
    sentry_activate
)
from epicevents.employee.manager_employee import EpicManagerEmployee
from epicevents.client.client_views import ClientView
from epicevents.employee.employee_views import EmployeeView


class EpicManagerClient():

    def __init__(self, user, base):
        self.user = user
        self.epic = base
        self.controller_employee = EpicManagerEmployee(self.user, self.epic)

    def choice_client(self, commercial_name) -> str:
        """
            - ask to confirm a client selection
            - read database
            - ask to select a client

        Args:
            commercial_name (str): commercial username

        Returns:
            str: client full_name
        """
        client = None
        # select a client
        result = ClientView.prompt_confirm_client()
        if result:
            employees = self.epic.dbclients.get_clients(commercial_name)
            clients_name = [c.full_name for c in employees]
            client = ClientView.prompt_client(clients_name)
        return client

    @sentry_activate
    @is_authenticated
    def list_of_clients(self) -> None:
        """
            - offers to choose a commercial
            - read database and display data
        """
        cname = self.controller_employee.choice_commercial()
        clients = self.epic.dbclients.get_clients(cname)
        ClientView.display_list_clients(clients)

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_client_commercial(self) -> None:
        """
            - ask to choose a client
            - ask to choose a commercial
            - update database
        """
        clients = self.epic.dbclients.get_clients()
        clients = [c.full_name for c in clients]
        client = ClientView.prompt_client(clients)
        commercials = self.epic.dbemployees.get_commercials()
        commercials = [c.username for c in commercials]
        ename = EmployeeView.prompt_commercial(commercials)
        self.epic.dbclients.update_commercial(client, ename)

    @sentry_activate
    @is_authenticated
    @is_commercial
    def create_client(self) -> None:
        """
            - ask data of client
            - select a random manager
            - send a task to the manager for creating the contract
        """
        data = ClientView.prompt_data_client()
        self.epic.dbclients.create(self.user.username, data)
        managers = self.epic.dbemployees.get_managers()
        e = random.choice(managers)
        text = 'Creer le contrat du client ' + data['full_name']
        self.epic.dbemployees.create_task(e.username, text)

    @sentry_activate
    @is_authenticated
    @is_commercial
    def update_client(self):
        """
            - ask a select of a client in the clients of user list
            - display client information
            - ask for the new data
            - update databse
            - display new client information
        """
        clients = self.epic.dbclients.get_clients(
            commercial_name=self.user.username)
        clients = [c.full_name for c in clients]
        client_name = ClientView.prompt_client(clients)
        client = self.epic.dbclients.get(client_name)
        ClientView.display_client_info(client)
        data = ClientView.prompt_data_client(full_name_required=False)
        client_name = self.epic.dbclients.update(client_name, data)
        print(f'get {client_name}')
        client = self.epic.dbclients.get(client_name)
        ClientView.display_client_info(client)
