import jwt
from sentry_sdk import capture_exception
from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import ErrorView
from epicevents.views.menu_views import menu_choice, menu_update_contract
from epicevents.views.contract_views import ContractView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.event_views import EventView
from epicevents.views.data_views import DataView
from epicevents.views.prompt_views import PromptView
from .config import Config, Environ
from .databasetools import EpicDatabaseWithData
from .session import load_session, stop_session, create_session
from .decorators import (
    is_authenticated,
    is_commercial, is_manager, is_support)


class EpicManager:

    def __init__(self, args) -> None:

        self.args = args

        # load .env file
        db = Config()
        self.env = Environ()

        print(db)
        print(db.db_config)
        # create database
        self.epic = EpicDatabaseWithData(**db.db_config)

    def __str__(self) -> str:
        return "CRM EPIC EVENTS"

    def check_logout(self) -> bool:
        """
        Stop the current session
        Returns:
            bool: always return True
        """
        if self.args.logout:
            stop_session()
            display_logout()
        return True

    def check_login(self) -> bool:
        if self.args.login:
            stop_session()
            (username, password) = self.args.login.split('/')
            e = self.epic.check_connection(username, password)
            if e:
                create_session(e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)
            else:
                ErrorView.display_error_login()

    @is_authenticated
    def check_session(self):
        token = load_session()
        user_info = jwt.decode(
                        token, self.env.SECRET_KEY, algorithms=['HS256'])
        username = user_info['username']
        e = self.epic.check_employee(username)
        if e:
            return e
        else:
            ErrorView.display_error_login()
            return None

    def choice_commercial(self) -> str:
        # select a commercial
        cname = None
        result = EmployeeView.prompt_confirm_commercial()
        if result:
            commercials = self.epic.dbemployees.get_commercials()
            commercials_name = [c.username for c in commercials]
            cname = EmployeeView.prompt_commercial(commercials_name)
        return cname

    def choice_client(self, commercial_name) -> str:
        client = None
        # select a client
        result = ClientView.prompt_confirm_client()
        if result:
            employees = self.epic.dbclients.get_clients(commercial_name)
            clients_name = [c.full_name for c in employees]
            client = ClientView.prompt_client(clients_name)
        return client

    @is_authenticated
    def list_of_clients(self):
        try:
            cname = self.choice_commercial()
            clients = self.epic.dbclients.get_clients(cname)
            ClientView.display_list_clients(clients)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    def list_of_contracts(self):
        try:
            state = None
            cname = self.choice_commercial()
            client = self.choice_client(cname)
            # select a state
            result = PromptView.prompt_confirm_statut()
            if result:
                states = self.epic.dbcontracts.get_states()
                state = PromptView.prompt_statut(states)
            # display list
            ContractView.display_list_contracts(
                self.epic.dbcontracts.get_contracts(cname, client, state))
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    def list_of_events(self):
        try:
            contract_ref = None
            sname = None
            cname = self.choice_commercial()
            client = self.choice_client(cname)
            # select a contract
            result = ContractView.prompt_confirm_contract()
            if result:
                contracts = self.epic.dbcontracts.get_contracts(cname, client)
                contracts_ref = [c.ref for c in contracts]
                contract_ref = ContractView.prompt_contract(contracts_ref)
            # select a support
            result = EmployeeView.prompt_confirm_support()
            if result:
                supports = self.epic.dbemployees.get_supports()
                supports_name = [c.username for c in supports]
                supports_name.append('-- sans support --')
                sname = EmployeeView.prompt_support(supports_name)
            # display list
            events = self.epic.dbevents.get_events(
                cname, client, contract_ref, sname)
            EventView.display_list_events(events)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    def list_of_task(self, e):
        try:
            tasks = self.epic.dbemployees.get_tasks(e)
            EmployeeView.display_list_tasks(tasks)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    def terminate_a_task(self, e):
        try:
            result = EmployeeView.prompt_confirm_task()
            if result:
                all_tasks_id = []
                for t in self.epic.dbemployees.get_tasks(e):
                    all_tasks_id.append(str(t.id))
                task = EmployeeView.prompt_task(all_tasks_id)
                self.epic.dbemployees.terminate_task(task)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    def show_profil(self, e):
        try:
            tasks = self.epic.dbemployees.get_tasks(e)
            DataView.display_profil(e, len(tasks))
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    def update_profil(self, e):
        try:
            result = EmployeeView.prompt_confirm_profil()
            if result:
                profil = EmployeeView.prompt_data_profil()
                self.epic.dbemployees.update_profil(e, profil)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def list_of_employees(self):
        try:
            employees = self.epic.dbemployees.get_employees()
            EmployeeView.display_list_employees(employees)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def create_new_employee(self):
        roles = self.epic.dbemployees.get_roles()
        try:
            data = EmployeeView.prompt_data_employee(roles)
            self.epic.dbemployees.create_employee(data)
        except KeyboardInterrupt:
            DataView.display_interupt()
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def update_employee_role(self):
        try:
            employees = self.epic.dbemployees.get_employees()
            enames = [e.username for e in employees]
            ename = EmployeeView.prompt_employee(enames)
            roles = self.epic.dbemployees.get_roles()
            role = EmployeeView.prompt_role(roles)
            self.epic.dbemployees.update_employee(ename, role)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def inactivate_employee(self):
        try:
            employees = self.epic.dbemployees.get_employees()
            enames = [e.username for e in employees]
            ename = EmployeeView.prompt_employee(enames)
            self.epic.dbemployees.inactivate(ename)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def create_contract(self):
        clients = self.epic.dbclients.get_clients()
        enames = [c.full_name for c in clients]
        ename = ClientView.prompt_client(enames)
        try:
            data = ContractView.prompt_data_contract()
            self.epic.dbcontracts.create(ename, data)
        except KeyboardInterrupt:
            DataView.display_interupt()
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def update_contract(self):
        contracts = self.epic.dbcontracts.get_active_contracts()
        refs = [c.ref for c in contracts]
        ref = ContractView.prompt_contract(refs)
        state = self.epic.dbcontracts.get_state(ref)
        try:
            choice = menu_update_contract(state)
            match choice:
                case 1:
                    try:
                        data = PromptView.prompt_data_paiement()
                        self.epic.dbcontracts.add_paiement(ref, data)
                    except KeyboardInterrupt:
                        DataView.display_interupt()
                case 2:
                    try:
                        data = ContractView.prompt_data_contract()
                        self.epic.dbcontracts.update(ref, data)
                    except KeyboardInterrupt:
                        DataView.display_interupt()
                case 3:
                    self.epic.dbcontracts.cancel(ref)
        except KeyboardInterrupt:
            DataView.display_interupt()
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def update_client_commercial(self):
        try:
            clients = self.epic.dbclients.get_clients()
            clients = [c.full_name for c in clients]
            client = ClientView.prompt_client(clients)
            commercials = self.epic.dbemployees.get_commercials()
            commercials = [c.username for c in commercials]
            ename = EmployeeView.prompt_commercial(commercials)
            self.epic.dbclients.update_commercial(client, ename)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_manager
    def update_event(self):
        try:
            supports = self.epic.dbemployees.get_supports()
            supports = [s.username for s in supports]
            support = EmployeeView.prompt_support(supports)
            contracts = self.epic.dbcontracts.get_active_contracts()
            contracts = [c.ref for c in contracts]
            contract = ContractView.prompt_contract(contracts)
            events = self.epic.dbevents.get_events(
                contract_ref=contract, state_code='U')
            events = [e.title for e in events]
            event = EventView.prompt_event(events)
            self.epic.dbevents.update(contract, event, support)
        except KeyboardInterrupt:
            DataView.display_interupt()
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_commercial
    def create_client(self, e):
        try:
            data = ClientView.prompt_data_client()
            self.epic.dbclients.create(e.username, data)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_commercial
    def update_client(self, e):
        try:
            clients = self.epic.dbclients.get_clients(
                commercial_name=e.username)
            clients = [c.full_name for c in clients]
            client = ClientView.prompt_client(clients)
            data = ClientView.prompt_data_client()
            self.epic.dbclients.update(client, data)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_commercial
    def create_event(self, e):
        try:
            contracts = self.epic.dbcontracts.get_contracts(
                commercial_name=e.username, state_value='S')
            contracts = [c.ref for c in contracts]
            contract = ContractView.prompt_contract(contracts)
            types = self.epic.dbevents.get_types()
            types = [r.title for r in types]
            type = EventView.prompt_type(types)
            data = EventView.prompt_data_event()
            self.epic.dbevents.create(contract, type, data)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_commercial
    def add_task_create_contract(self, e):
        try:
            managers = self.epic.dbemployees.get_managers()
            managers = [e.username for e in managers]
            manager = EmployeeView.prompt_manager(managers)
            clients = self.epic.dbclients.get_clients(
                commercial_name=e.username)
            clients = [c.full_name for c in clients]
            client = ClientView.prompt_client(clients)
            self.epic.dbemployees.create_task_add_contract(manager, client)
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_support
    def terminate_event(self, e):
        try:
            events = self.epic.dbevents.get_events(
                support_name=e.username, state_code='U')
            events = [f'{e.contract.ref}|{e.title}' for e in events]
            if events:
                try:
                    event = EventView.prompt_event(events)
                    rapport = EventView.prompt_rapport()
                    self.epic.dbevents.terminate(event, rapport)
                except KeyboardInterrupt:
                    DataView.display_interupt()
            else:
                EventView.display_no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()
        except Exception as e:
            capture_exception(e)

    @is_authenticated
    @is_support
    def cancel_event(self, e):
        try:
            events = self.epic.dbevents.get_events(
                support_name=e.username, state_code='U')
            events = [f'{e.contract.ref}|{e.title}' for e in events]
            if events:
                try:
                    event = EventView.prompt_event(events)
                    self.epic.dbevents.cancel(event)
                except KeyboardInterrupt:
                    DataView.display_interupt()
            else:
                EventView.display_no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()
        except Exception as e:
            capture_exception(e)

    def run(self) -> None:

        self.check_logout()
        self.check_login()
        e = self.check_session()
        if e:
            running = True
            display_welcome(e.username)
            self.list_of_task(e)
            try:
                while running:
                    result = menu_choice(e.role.code)
                    match result:
                        case '01':
                            self.show_profil(e)
                            self.update_profil(e)
                        case '02':
                            self.list_of_task(e)
                            self.terminate_a_task(e)
                        case '03':
                            self.list_of_clients()
                        case '04':
                            self.list_of_contracts()
                        case '05':
                            self.list_of_events()
                        case '06':
                            match e.role.code:
                                case 'M':
                                    self.list_of_employees()
                                case 'C':
                                    self.create_client(e)
                                case 'S':
                                    self.terminate_event(e)
                        case '07':
                            match e.role.code:
                                case 'M':
                                    self.create_new_employee()
                                case 'C':
                                    self.update_client(e)
                                case 'S':
                                    self.cancel_event(e)
                        case '08':
                            match e.role.code:
                                case 'M':
                                    self.update_employee_role()
                                case 'C':
                                    self.create_event(e)
                        case '09':
                            match e.role.code:
                                case 'M':
                                    self.inactivate_employee()
                                case 'C':
                                    self.add_task_create_contract(e)
                        case '10':
                            self.create_contract()
                        case '11':
                            self.update_contract()
                        case '12':
                            self.update_client_commercial()
                        case '13':
                            self.update_event()
                        case 'D':
                            stop_session()
                            running = False
                        case 'Q':
                            running = False
                            create_session(
                                e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)
                    create_session(
                                e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)

            except KeyboardInterrupt:
                pass
