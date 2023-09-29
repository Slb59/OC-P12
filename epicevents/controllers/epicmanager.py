import jwt
from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import ErrorView
from epicevents.views.menu_views import menu_choice, menu_update_contract
from epicevents.views.contract_views import ContractView
from epicevents.views.list_views import DisplayView
from epicevents.views.data_views import DataView
from epicevents.views.prompt_views import PromptView
from .config import Config, Environ
from .databasetools import EpicDatabaseWithData
from .session import load_session, stop_session, create_session
from .decorators import (
    is_authenticated,
    # is_commercial,
    is_manager,
    # is_support
)


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
        result = PromptView.prompt_confirm_commercial()
        if result:
            commercials = self.epic.dbemployees.get_commercials()
            commercials_name = [c.username for c in commercials]
            cname = PromptView.prompt_commercial(commercials_name)
        return cname

    def choice_client(self, commercial_name) -> str:
        client = None
        # select a client
        result = PromptView.prompt_confirm_client()
        if result:
            employees = self.epic.dbclients.get_clients(commercial_name)
            clients_name = [c.full_name for c in employees]
            client = PromptView.prompt_client(clients_name)
        return client

    @is_authenticated
    def list_of_clients(self):
        cname = self.choice_commercial()
        clients = self.epic.dbclients.get_clients(cname)
        DisplayView.display_list_clients(clients)

    @is_authenticated
    def list_of_contracts(self):
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

    @is_authenticated
    def list_of_events(self):
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
        result = PromptView.prompt_confirm_support()
        if result:
            supports = self.epic.dbemployees.get_supports()
            supports_name = [c.username for c in supports]
            supports_name.append('-- sans support --')
            sname = PromptView.prompt_support(supports_name)
        # display list
        events = self.epic.get_events(cname, client, contract_ref, sname)
        DisplayView.display_list_events(events)

    @is_authenticated
    def list_of_task(self, e):
        tasks = self.epic.dbemployees.get_tasks(e)
        DisplayView.display_list_tasks(tasks)

    @is_authenticated
    def terminate_a_task(self, e):
        result = PromptView.prompt_confirm_task()
        if result:
            all_tasks_id = []
            for t in self.epic.dbemployees.get_tasks(e):
                all_tasks_id.append(str(t.id))
            task = PromptView.prompt_task(all_tasks_id)
            self.epic.dbemployees.terminate_task(task)

    @is_authenticated
    def show_profil(self, e):
        tasks = self.epic.dbemployees.get_tasks(e)
        DataView.display_profil(e, len(tasks))

    @is_authenticated
    def update_profil(self, e):
        result = PromptView.prompt_confirm_profil()
        if result:
            profil = PromptView.prompt_data_profil()
            self.epic.dbemployees.update_profil(e, profil)

    @is_authenticated
    @is_manager
    def list_of_employees(self):
        employees = self.epic.dbemployees.get_employees()
        DisplayView.display_list_employees(employees)

    @is_authenticated
    @is_manager
    def create_new_employee(self):
        roles = self.epic.dbemployees.get_roles()
        try:
            data = PromptView.prompt_data_employee(roles)
            self.epic.dbemployees.create_employee(data)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @is_authenticated
    @is_manager
    def update_employee_role(self):
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = PromptView.prompt_employee(enames)
        roles = self.epic.dbemployees.get_roles()
        role = PromptView.prompt_role(roles)
        self.epic.dbemployees.update_employee(ename, role)

    @is_authenticated
    @is_manager
    def inactivate_employee(self):
        employees = self.epic.dbemployees.get_employees()
        enames = [e.username for e in employees]
        ename = PromptView.prompt_employee(enames)
        self.epic.dbemployees.inactivate(ename)

    @is_authenticated
    @is_manager
    def create_contract(self):
        clients = self.epic.dbclients.get_clients()
        enames = [c.full_name for c in clients]
        ename = PromptView.prompt_client(enames)
        try:
            data = ContractView.prompt_data_contract()
            self.epic.dbcontracts.create(ename, data)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @is_authenticated
    @is_manager
    def update_contract(self):
        contracts = self.epic.dbcontracts.get_active_contracts()
        refs = [c.ref for c in contracts]
        ref = ContractView.prompt_contract(refs)
        choice = menu_update_contract()
        match choice:
            case 1:
                try:
                    data = PromptView.prompt_data_paiement()
                    self.epic.dbcontracts.add_paiement(ref, data)
                except KeyboardInterrupt:
                    DataView.display_interupt()
            case 2:
                state = self.epic.dbcontracts.get_state(ref)
                if state == 'C':
                    try:
                        data = ContractView.prompt_data_contract()
                        self.epic.dbcontracts.update(ref, data)
                    except KeyboardInterrupt:
                        DataView.display_interupt()
                else:
                    DataView.display_error_contract_need_c()

    @is_authenticated
    @is_manager
    def update_client(self):
        clients = self.epic.dbclients.get_clients()
        clients = [c.full_name for c in clients]
        client = PromptView.prompt_client(clients)
        commercials = self.epic.dbemployees.get_commercials()
        commercials = [c.username for c in commercials]
        ename = PromptView.prompt_commercial(commercials)
        self.epic.dbclients.update_commercial(client, ename)

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
                                    ...  # creer un nouveau client
                                case 'S':
                                    ...  # cloturer un evenement
                        case '07':
                            match e.role.code:
                                case 'M':
                                    self.create_new_employee()
                                case 'C':
                                    ...
                        case '08':
                            match e.role.code:
                                case 'M':
                                    self.update_employee_role()
                                case 'C':
                                    ...  # creer un evenement
                        case '09':
                            match e.role.code:
                                case 'M':
                                    self.inactivate_employee()
                                case 'C':
                                    ...  #
                        case '10':
                            self.create_contract()
                        case '11':
                            self.update_contract()
                        case '12':
                            self.update_client()
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
