from epicevents.controllers.epicmanager import EpicManager
from epicevents.employee.manager_employee import (
    EpicManagerEmployee, EpicManagerTask)
from epicevents.client.manager_client import EpicManagerClient
from epicevents.contract.manager_contract import EpicManagerContract
from epicevents.event.manager_event import EpicManagerEvent
from .session import stop_session

from epicevents.views.auth_views import AuthView
from epicevents.views.menu_views import MenuView


class EpicManagerDashboard():

    def __init__(self) -> None:
        self.manager = EpicManager()
        self.manager_employee = EpicManagerEmployee(
            self.manager.user, self.manager.epic)
        self.manager_task = EpicManagerTask(
            self.manager.user, self.manager.epic)
        self.manager_client = EpicManagerClient(
            self.manager.user, self.manager.epic)
        self.manager_contract = EpicManagerContract(
            self.manager.user, self.manager.epic)
        self.manager_event = EpicManagerEvent(
            self.manager.user, self.manager.epic)

    def call_function(self, choice) -> bool:
        match choice:
            case '01':
                self.manager_employee.show_profil()
                self.manager_employee.update_profil()
            case '02':
                self.manager_task.list_of_task()
                self.manager_task.terminate_a_task()
            case '03':
                self.manager_client.list_of_clients()
            case '04':
                self.manager_contract.list_of_contracts()
            case '05':
                self.manager_event.list_of_events()
            case '06':
                match self.user.role.code:
                    case 'M':
                        self.manager_employee.list_of_employees()
                    case 'C':
                        self.manager_client.create_client()
                    case 'S':
                        self.manager_event.terminate_event()
            case '07':
                match self.user.role.code:
                    case 'M':
                        self.manager_employee.create_new_employee()
                    case 'C':
                        self.manager_client.update_client()
                    case 'S':
                        self.manager_event.cancel_event()
            case '08':
                match self.user.role.code:
                    case 'M':
                        self.manager_employee.update_employee_role()
                    case 'C':
                        self.manager_event.create_event()
            case '09':
                match self.user.role.code:
                    case 'M':
                        self.manager_employee.inactivate_employee()
                    case 'C':
                        self.manager_task.add_task_create_contract()
            case '10':
                self.manager_contract.create_contract()
            case '11':
                self.manager_contract.update_contract()
            case '12':
                self.manager_client.update_client_commercial()
            case '13':
                self.manager_event.update_event()
            case 'D':
                stop_session()
                return False
            case 'Q':
                self.manager.refresh_session()
                return False
        return True

    def run(self) -> None:

        if self.manager.user:
            running = True
            AuthView.display_welcome(self.manager.user.username)
            self.manager_task.list_of_task()
            try:
                while running:
                    result = MenuView.menu_choice(self.manager.user.role.code)
                    running = self.call_function(result)

            except KeyboardInterrupt:
                pass
