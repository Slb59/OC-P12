import jwt
import random
from epicevents.views.auth_views import AuthView
from epicevents.views.error import ErrorView
from epicevents.views.menu_views import menu_choice, menu_update_contract
from epicevents.views.contract_views import ContractView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.event_views import EventView
from epicevents.views.data_views import DataView
from epicevents.views.prompt_views import PromptView

from .config import Config, Environ, create_config
from .databasetools import EpicDatabase, EpicDatabaseWithData
from .session import load_session, stop_session, create_session
from .decorators import (
    is_authenticated,
    is_commercial, is_manager, is_support,
    sentry_activate)


class EpicManager:

    def __init__(self) -> None:

        # load .env file
        db = Config()
        self.env = Environ()

        # create database
        self.epic = EpicDatabase(**db.db_config)
        self.user = self.check_session()

    def __str__(self) -> str:
        return "CRM EPIC EVENTS"

    @is_authenticated
    def check_logout(self) -> bool:
        """
        Stop the current session
        Returns:
            bool: always return True
        """
        stop_session()
        AuthView.display_logout()
        return True

    @sentry_activate
    def login(self) -> bool:
        stop_session()
        (username, password) = AuthView.prompt_login()
        e = self.epic.check_connection(username, password)
        if e:
            create_session(e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)
        else:
            ErrorView.display_error_login()

    @sentry_activate
    def check_session(self):
        token = load_session()
        if token:
            user_info = jwt.decode(
                            token, self.env.SECRET_KEY, algorithms=['HS256'])
            username = user_info['username']
            e = self.epic.check_employee(username)
            if e:
                return e

    def refresh_session(self):
        create_session(self.user, self.env.TOKEN_DELTA, self.env.SECRET_KEY)

    @classmethod
    def initbase(cls):
        stop_session()
        values = AuthView.prompt_baseinit()
        create_config(*values)
        db = Config()
        result = AuthView.prompt_confirm_testdata()
        if result:
            EpicDatabaseWithData(**db.db_config)
        else:
            EpicDatabase(**db.db_config)
        AuthView.display_database_connection(values[0])

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

    @sentry_activate
    @is_authenticated
    def list_of_clients(self):
        cname = self.choice_commercial()
        clients = self.epic.dbclients.get_clients(cname)
        ClientView.display_list_clients(clients)

    @sentry_activate
    @is_authenticated
    def list_of_contracts(self):
        state = None
        cname = self.choice_commercial()
        client = self.choice_client(cname)
        # select a state
        result = PromptView.prompt_confirm_statut()
        if result:
            states = self.epic.dbcontracts.get_states()
            try:
                state = PromptView.prompt_select(
                    ContractView.select_statut(), states)
            except KeyboardInterrupt:
                state = None
        # display list
        ContractView.display_list_contracts(
            self.epic.dbcontracts.get_contracts(cname, client, state))

    @sentry_activate
    @is_authenticated
    def list_of_events(self):
        contract_ref = None
        sname = None
        cname = self.choice_commercial()
        client = self.choice_client(cname)
        # select a contract
        result = ContractView.prompt_confirm_contract()
        if result:
            contracts = self.epic.dbcontracts.get_contracts(
                cname, client)
            contracts_ref = [c.ref for c in contracts]
            contract_ref = PromptView.prompt_select(
                ContractView.select_contract(), contracts_ref)
        # select a support
        result = EmployeeView.prompt_confirm_support()
        if result:
            supports = self.epic.dbemployees.get_supports()
            supports_name = [c.username for c in supports]
            supports_name.append(EventView.no_support())
            sname = PromptView.prompt_select(
                EmployeeView.select_support(), supports_name)
        # display list
        events = self.epic.dbevents.get_events(
            cname, client, contract_ref, sname)
        EventView.display_list_events(events)

    @sentry_activate
    @is_authenticated
    def list_of_task(self):
        tasks = self.epic.dbemployees.get_tasks(self.user)
        EmployeeView.display_list_tasks(tasks)

    @sentry_activate
    @is_authenticated
    def terminate_a_task(self):
        result = EmployeeView.prompt_confirm_task()
        if result:
            all_tasks_id = []
            for t in self.epic.dbemployees.get_tasks(self.user):
                all_tasks_id.append(str(t.id))
            try:
                task = PromptView.prompt_select(
                    EmployeeView.select_task(), all_tasks_id)
                self.epic.dbemployees.terminate_task(task)
                DataView.display_data_update()
            except KeyboardInterrupt:
                DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    def show_profil(self):
        tasks = self.epic.dbemployees.get_tasks(self.user)
        DataView.display_profil(self.user, len(tasks))

    @sentry_activate
    @is_authenticated
    def update_profil(self):
        result = EmployeeView.prompt_confirm_profil()
        if result:
            profil = EmployeeView.prompt_data_profil()
            self.epic.dbemployees.update_profil(self.user, profil)
            DataView.display_data_update()

    @sentry_activate
    @is_authenticated
    @is_manager
    def list_of_employees(self):
        employees = self.epic.dbemployees.get_employees()
        EmployeeView.display_list_employees(employees)

    @sentry_activate
    @is_authenticated
    @is_manager
    def create_new_employee(self):
        roles = self.epic.dbemployees.get_roles()
        try:
            data = EmployeeView.prompt_data_employee(roles)
            self.epic.dbemployees.create_employee(data)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_employee_role(self):
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = EmployeeView.prompt_employee(enames)
        roles = self.epic.dbemployees.get_roles()
        role = EmployeeView.prompt_role(roles)
        self.epic.dbemployees.update_employee(ename, role=role)

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_employee_password(self):
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = EmployeeView.prompt_employee(enames)
        password = EmployeeView.prompt_password()
        self.epic.dbemployees.update_employee(ename, password=password)

    @sentry_activate
    @is_authenticated
    @is_manager
    def inactivate_employee(self):
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = EmployeeView.prompt_employee(enames)
        self.epic.dbemployees.inactivate(ename)

    @sentry_activate
    @is_authenticated
    @is_manager
    def create_contract(self):
        clients = self.epic.dbclients.get_clients()
        enames = [c.full_name for c in clients]
        ename = ClientView.prompt_client(enames)
        try:
            data = ContractView.prompt_data_contract()
            self.epic.dbcontracts.create(ename, data)
            contract_ref = data['ref']
            text = f'Contrat {contract_ref} en attente de signature'
            self.epic.dbemployees.create_task(self.user.username, text)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
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
                    self.epic.dbcontracts.signed(ref)
                    text = f'Creer les évènements du contrat {ref}'
                    contract = self.epic.dbcontracts.get(ref)
                    DataView.display_workflow()
                    self.epic.dbemployees.create_task(
                        contract.client.commercial.username, text)
                case 4:
                    self.epic.dbcontracts.cancel(ref)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_client_commercial(self):
        clients = self.epic.dbclients.get_clients()
        clients = [c.full_name for c in clients]
        client = ClientView.prompt_client(clients)
        commercials = self.epic.dbemployees.get_commercials()
        commercials = [c.username for c in commercials]
        ename = EmployeeView.prompt_commercial(commercials)
        self.epic.dbclients.update_commercial(client, ename)

    @is_authenticated
    @is_manager
    def update_event(self):
        try:
            supports = self.epic.dbemployees.get_supports()
            supports = [s.username for s in supports]
            support = PromptView.prompt_select(
                EmployeeView.select_support(), supports)
            contracts = self.epic.dbcontracts.get_active_contracts()
            contracts = [c.ref for c in contracts]
            contract = PromptView.prompt_select(
                ContractView.select_contract(), contracts)
            events = self.epic.dbevents.get_events(
                contract_ref=contract, state_code='U',
                support_name=EventView.no_support())
            events = [e.title for e in events]
            if events:
                event_title = PromptView.prompt_select(
                    EventView.select_event(), events)
                self.epic.dbevents.update(contract, event_title, support)
                DataView.display_workflow()
                self.epic.dbemployees.create_task(
                    support,
                    EventView.workflow_affect(event_title)
                )
            else:
                EventView.no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_commercial
    def create_client(self):
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
        clients = self.epic.dbclients.get_clients(
            commercial_name=self.user.username)
        clients = [c.full_name for c in clients]
        client = ClientView.prompt_client(clients)
        data = ClientView.prompt_data_client()
        self.epic.dbclients.update(client, data)

    @sentry_activate
    @is_authenticated
    @is_commercial
    def create_event(self):
        contracts = self.epic.dbcontracts.get_contracts(
            commercial_name=self.user.username, state_value='S')
        if contracts:
            contracts = [c.ref for c in contracts]
            contract = PromptView.prompt_select(
                ContractView.select_contract(), contracts)
            types = self.epic.dbevents.get_types()
            types = [r.title for r in types]
            try:
                type = PromptView.prompt_select(
                    EventView.select_type_event(), types)
                data = EventView.prompt_data_event()
                self.epic.dbevents.create(contract, type, data)
                # workflow creation
                DataView.display_workflow()
                managers = self.epic.dbemployees.get_managers()
                manager = random.choice(managers)
                self.epic.dbemployees.create_task(
                    manager.username,
                    EventView.workflow_ask_affect(data['title']))
            except KeyboardInterrupt:
                DataView.display_interupt()
        else:
            DataView.display_nocontracts()

    @sentry_activate
    @is_authenticated
    @is_commercial
    def add_task_create_contract(self):
        managers = self.epic.dbemployees.get_managers()
        managers = [e.username for e in managers]
        manager = EmployeeView.prompt_manager(managers)
        clients = self.epic.dbclients.get_clients(
            commercial_name=self.user.username)
        clients = [c.full_name for c in clients]
        client = ClientView.prompt_client(clients)
        text = 'Creer le contrat du client ' + client
        self.epic.dbemployees.create_task(manager, text)

    @sentry_activate
    @is_authenticated
    @is_support
    def terminate_event(self):
        try:
            events = self.epic.dbevents.get_events(
                support_name=self.user.username, state_code='U')
            events = [f'{e.contract.ref}|{e.title}' for e in events]
            if events:
                try:
                    event = PromptView.prompt_select(
                        EventView.select_event(), events)
                    rapport = EventView.prompt_rapport()
                    self.epic.dbevents.terminate(event, rapport)
                except KeyboardInterrupt:
                    DataView.display_interupt()
            else:
                EventView.display_no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_support
    def cancel_event(self):
        try:
            events = self.epic.dbevents.get_events(
                support_name=self.user.username, state_code='U')
            events = [f'{e.contract.ref}|{e.title}' for e in events]
            if events:
                try:
                    event = PromptView.prompt_select(
                        EventView.select_event(), events)
                    self.epic.dbevents.cancel(event)
                except KeyboardInterrupt:
                    DataView.display_interupt()
            else:
                EventView.display_no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()

    def run(self) -> None:

        if self.user:
            running = True
            AuthView.display_welcome(self.user.username)
            self.list_of_task()
            try:
                while running:
                    result = menu_choice(self.user.role.code)
                    match result:
                        case '01':
                            self.show_profil()
                            self.update_profil()
                        case '02':
                            self.list_of_task()
                            self.terminate_a_task()
                        case '03':
                            self.list_of_clients()
                        case '04':
                            self.list_of_contracts()
                        case '05':
                            self.list_of_events()
                        case '06':
                            match self.user.role.code:
                                case 'M':
                                    self.list_of_employees()
                                case 'C':
                                    self.create_client()
                                case 'S':
                                    self.terminate_event()
                        case '07':
                            match self.user.role.code:
                                case 'M':
                                    self.create_new_employee()
                                case 'C':
                                    self.update_client()
                                case 'S':
                                    self.cancel_event()
                        case '08':
                            match self.user.role.code:
                                case 'M':
                                    self.update_employee_role()
                                case 'C':
                                    self.create_event()
                        case '09':
                            match self.user.role.code:
                                case 'M':
                                    self.inactivate_employee()
                                case 'C':
                                    self.add_task_create_contract()
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
                            self.refresh_session()

            except KeyboardInterrupt:
                pass
