from sentry_sdk import capture_exception
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
    Employee, EventType
    )
from epicevents.views.auth_views import AuthView
from epicevents.employee.employee_base import EmployeeBase
from epicevents.client.client_base import ClientBase
from epicevents.contract.contract_base import ContractBase
from epicevents.event.event_base import EventBase


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

        print(f'checking {self.url} ...')
        try:
            if database_exists(self.url):
                AuthView.display_database_connection(database)
            else:
                data_manager = AuthView.prompt_manager()
                AuthView.display_waiting_databasecreation(
                    self.database_creation, data_manager)
        except Exception:
            data_manager = AuthView.prompt_manager()
            AuthView.display_waiting_databasecreation(
                self.database_creation, data_manager)

        self.name = database
        self.engine = create_engine(self.url)

        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.dbemployees = EmployeeBase(self.session)
        self.dbclients = ClientBase(self.session)
        self.dbcontracts = ContractBase(self.session)
        self.dbevents = EventBase(self.session)

    def __str__(self) -> str:
        return f'{self.name} database'

    def database_disconnect(self):
        self.session.close()
        self.engine.dispose()

    def database_creation(self, username, password):
        create_database(self.url)
        # init database structure
        engine = create_engine(self.url)
        Base.metadata.create_all(engine)
        self.session = scoped_session(sessionmaker(bind=engine))
        self.dbemployees = EmployeeBase(self.session)
        # add initial data
        self.first_initdb(username, password)
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
        if e:
            try:
                if self.dbemployees.ph.verify(e.password, password):
                    AuthView.display_database_connection(self.name)
                    return e
            except VerifyMismatchError as e:
                capture_exception(e)
        else:
            return None

    def check_employee(self, username) -> Employee:
        """
        Check the username is in database employee
        Args:
            username (str): the username
        Returns:
            Employee: an instance of Employee
        """
        return Employee.find_by_username(self.session, username)

    def first_initdb(self, username, password):
        # add departments
        management_dpt = Department(name='management department')
        support_dpt = Department(name='support department')
        commercial_dpt = Department(name='commercial department')
        self.session.add_all([management_dpt, support_dpt, commercial_dpt])
        # add a superuser
        self.dbemployees.add_employee(username, password, 'Manager')
        # add types of events
        event_type1 = EventType(title='conference')
        event_type2 = EventType(title='forum')
        event_type3 = EventType(title='show')
        event_type4 = EventType(title='seminar')
        self.session.add_all(
            [event_type1, event_type2, event_type3, event_type4]
            )
        self.session.commit()
