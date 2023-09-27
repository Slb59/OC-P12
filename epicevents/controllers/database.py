from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy_utils.functions import (
    database_exists,
    create_database
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
    )
from epicevents.models.entities import (
    Base, Department,
    Employee, Commercial,
    Client, Contract, Event,
    EventType, Task
    )
from epicevents.views.auth_views import (
    display_waiting_databasecreation,
    display_database_connection
)
from epicevents.controllers.employee_base import EmployeeBase


class EpicDatabase:

    """ connect on db and manage crud operations """

    def __init__(self, database, host, user, password, port) -> None:

        self.url = URL.create(
            drivername="postgresql",
            database=database,
            host=host,
            username=user,
            password=password,
            port=int(port)
        )

        self.ph = PasswordHasher()

        print(f'checking {self.url} ...')
        try:
            if database_exists(self.url):
                display_database_connection(database)
            else:
                display_waiting_databasecreation(self.database_creation)
        except Exception:
            display_waiting_databasecreation(self.database_creation)

        self.name = database
        self.engine = create_engine(self.url)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.dbemployees = EmployeeBase(self.session)

    def __str__(self) -> str:
        return f'{self.name} database'

    def database_creation(self):
        create_database(self.url)
        # init database structure
        engine = create_engine(self.url)
        Base.metadata.create_all(engine)
        self.session = scoped_session(sessionmaker(bind=engine))
        self.dbemployees = EmployeeBase(self.session)
        # add initial data
        self.first_initdb()
        self.session.remove()

    def check_connection(self, username, password) -> Employee:
        """
        Check the username/password is in database employee

        Args:
            username (str): the username
            password (str): the password

        Returns:
            Employee: an instance of Employee
        """
        e = Employee.find_by_username(self.session, username)
        try:
            if self.ph.verify(e.password, password):
                return e
            else:
                return None
        except VerifyMismatchError:
            return None

    def check_employee(self, username) -> Employee:
        """
        Check the username/password is in database employee

        Args:
            username (str): the username
            password (str): the password is encrypted

        Returns:
            Employee: an instance of Employee
        """
        print(f'-----> check employee {username}')
        return Employee.find_by_username(self.session, username)

    def first_initdb(self):
        # add departments
        management_dpt = Department(name='management department')
        support_dpt = Department(name='support department')
        commercial_dpt = Department(name='commercial department')
        self.session.add_all([management_dpt, support_dpt, commercial_dpt])
        # add a superuser
        self.dbemployees.add_employee('Osynia', 'osyA!111', 'Manager')
        # add types of events
        event_type1 = EventType(title='conference')
        event_type2 = EventType(title='forum')
        event_type3 = EventType(title='show')
        event_type4 = EventType(title='seminar')
        self.session.add_all(
            [event_type1, event_type2, event_type3, event_type4]
            )
        self.session.commit()

    def get_clients(self, commercial_name=''):
        if commercial_name:
            e = Commercial.find_by_username(self.session, commercial_name)
            result = e.clients
        else:
            result = Client.getall(self.session)
        return result

    def get_contracts_states(self):
        states = Contract.CONTRACT_STATES
        result = [s[1] for s in states]
        return result

    def get_contracts(
            self, commercial_name=None,
            client_name=None,
            state_value=None):
        state = None
        if state_value:
            states = Contract.CONTRACT_STATES
            for s in states:
                if state_value in s:
                    state = s[0]
        return Contract.find_by_selection(
            self.session, commercial_name, client_name, state)

    def get_events(
            self,
            commercial_name=None,
            client_name=None,
            contract_ref=None,
            support_name=None):
        if support_name == '-- sans support --':
            support_name = 'None'
        return Event.find_by_selection(
            self.session, commercial_name, client_name,
            contract_ref, support_name
        )

    def get_tasks(self, e):
        return Task.find_active_tasks(self.session, e)

    def terminate_task(self, task_id):
        Task.terminate(self.session, task_id)
        self.session.commit()
