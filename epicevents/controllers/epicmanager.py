import jwt

from epicevents.views.auth_views import display_logout, display_welcome
from epicevents.views.error import ErrorView
from epicevents.views.menu_views import menu_choice
from epicevents.views.list_views import DisplayView
from epicevents.views.prompt_views import PromptView
from .config import Config, Environ
from .databasetools import EpicDatabaseWithData
from .session import load_session, stop_session, create_session
from .decorators import (
    is_authenticated,
    # is_commercial,
    # is_manager,
    # is_support
)


class EpicManager:

    def __init__(self, args) -> None:

        self.args = args

        # load .env file
        db = Config()
        self.env = Environ()

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
            commercials_name = []
            for c in self.epic.get_commercials():
                commercials_name.append(c.username)
            cname = PromptView.prompt_commercial(commercials_name)
        return cname

    def choice_client(self, commercial_name) -> str:
        client = None
        # select a client
        result = PromptView.prompt_confirm_client()
        if result:
            clients_name = []
            for c in self.epic.get_clients(commercial_name):
                clients_name.append(c.full_name)
            client = PromptView.prompt_client(clients_name)
        return client

    @is_authenticated
    def list_of_clients(self):
        cname = self.choice_commercial()
        DisplayView.display_list_clients(self.epic.get_clients(cname))

    @is_authenticated
    def list_of_contracts(self):
        state = None
        cname = self.choice_commercial()
        client = self.choice_client(cname)
        # select a state
        result = PromptView.prompt_confirm_statut()
        if result:
            state = PromptView.prompt_statut(self.epic.get_contracts_states())
        # display list
        DisplayView.display_list_contracts(
            self.epic.get_contracts(cname, client, state))

    @is_authenticated
    def list_of_events(self):
        contract_ref = None
        support_username = None
        cname = self.choice_commercial()
        client = self.choice_client(cname)
        # select a contract
        result = PromptView.prompt_confirm_contract()
        if result:
            contracts_ref = []
            for c in self.epic.get_contracts(cname, client):
                contracts_ref.append(c.ref)
            contract_ref = PromptView.prompt_contract(contracts_ref)
        # select a support
        result = PromptView.prompt_confirm_support()
        if result:
            supports = self.epic.get_supports()
            supports_name = []
            for c in supports:
                supports_name.append(c.username)
            support_username = PromptView.prompt_support(supports_name)
        # display list
        DisplayView.display_list_events(
            self.epic.get_events(
                cname, client, contract_ref, support_username))

    @is_authenticated
    def list_of_task(self, e):
        DisplayView.display_list_tasks(self.epic.get_tasks(e))

    @is_authenticated
    def terminate_a_task(self, e):
        result = PromptView.prompt_confirm_task()
        if result:
            all_tasks_id = []
            for t in self.epic.get_tasks(e):
                all_tasks_id.append(str(t.id))
            task = PromptView.prompt_task(all_tasks_id)
            self.epic.terminate_task(task)

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
                    result = menu_choice(e.role.value)

                    match result:
                        case '02':
                            self.list_of_task(e)
                            self.terminate_a_task(e)
                        case '03':
                            self.list_of_clients()
                        case '04':
                            self.list_of_contracts()
                        case '05':
                            self.list_of_events()
                        case 'D':
                            stop_session()
                            running = False
                        case 'Q':
                            running = False
                            create_session(
                                e, self.env.TOKEN_DELTA, self.env.SECRET_KEY)

            except KeyboardInterrupt:
                pass
