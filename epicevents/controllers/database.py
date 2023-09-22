from argon2 import PasswordHasher
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy_utils import (
    # database_exists,
    create_database, drop_database
)
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
    )
from sqlalchemy.exc import ProgrammingError
from epicevents.models.entities import (
    Base, Department, Manager,
    Employee, Commercial,
    Client, Contract, Event,
    EventType
    )
from epicevents.views.auth_views import display_waiting_databasecreation


class EpicDatabase:

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
        self.ph = PasswordHasher()

        try:
            drop_database(self.url)
        except ProgrammingError:
            ...

        # if not database_exists(url):
        if True:
            display_waiting_databasecreation(self.database_creation)

        self.name = database
        self.engine = create_engine(self.url)
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def __str__(self) -> str:
        return f'{self.name} database'

    def database_creation(self):
        create_database(self.url)
        # init database structure
        engine = create_engine(self.url)
        Base.metadata.create_all(engine)
        self.session = scoped_session(sessionmaker(bind=engine))
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
        if self.ph.verify(e.password, password):
            return e
        else:
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

    def add_employee(self, username, password, role):
        # hashed_password = password

        hashed_password = self.ph.hash(password)

        match role:
            case 'Manager':
                d = Department.find_by_name(
                    self.session, 'management department')
                e = Manager(
                    username=username,
                    password=hashed_password,
                    department_id=d.id,
                    role='M')
            case 'Commercial':
                d = Department.find_by_name(
                    self.session, 'commercial department')
                e = Manager(
                    username=username,
                    password=hashed_password,
                    department_id=d.id,
                    role='C')
        self.session.add(e)
        self.session.commit()

    def first_initdb(self):
        # add departments
        management_dpt = Department(name='management department')
        support_dpt = Department(name='support department')
        commercial_dpt = Department(name='commercial department')
        self.session.add_all([management_dpt, support_dpt, commercial_dpt])
        # add a superuser
        self.add_employee('Osynia', 'osyA!111', 'Manager')
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

    def get_contracts(self):
        result = Contract.getall(self.session)
        return result

    def get_events(self):
        result = Event.getall(self.session)
        return result

    def get_commercials(self):
        return Commercial.getall(self.session)
