import random
from argon2 import PasswordHasher
from datetime import datetime
from random import randint
# from passlib.hash import argon2
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
    Client, Contract
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
        self.create_a_test_database()
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
        self.session.commit()
        self.add_employee('Osynia', 'osyA!111', 'Manager')

    def create_a_test_database(self):
        self.add_some_clients()
        self.add_some_contracts()

    def add_some_contracts(self):
        clients = Client.getall(self.session)
        for c in clients:
            nb_of_contracts = randint(0, 10)
            for i in range(nb_of_contracts):
                contract_description = f"Contract {i} for {c.full_name}"
                dt = datetime.now().strftime('%Y%m%d-%H%M%S:%f')
                state = random.choice(Contract.CONTRACT_STATES)[0]
                new_contract = Contract(
                    ref=f"{dt}-{randint(1000, 9999)}",
                    description=contract_description,
                    client_id=c.id,
                    total_amount=randint(500, 30000),
                    state=state
                    )
                self.session.add(new_contract)
        self.session.commit()

    def add_some_clients(self):
        self.add_employee('Yuka', 'yuka!111', 'Commercial')  
        e1 = Commercial.find_by_username(self.session, 'Yuka')
        self.add_employee('Esumi', 'esumi!111', 'Commercial')
        e2 = Commercial.find_by_username(self.session, 'Esumi')        
        company_names = ['League Computing',
                         'Valley Dressing',
                         'Jumpstart Travel',
                         'Social bleu-ciel',
                         'Restaurants de la citadelle']
        for i in range(20):
            c = Client(
                full_name=f'Client n°{i}',
                email=f'Client{i}@example.com',
                phone=f'{randint(10,80)}.{randint(100,800)}.{randint(10,80)}',
                company_name=random.choice(company_names),
                commercial_id=random.choice([e1.id, e2.id])
            )
            self.session.add(c)
        self.session.commit()

    def get_clients(self):
        result = Client.getall(self.session)
        return result

    def get_contracts(self):
        result = Contract.getall(self.session)
        return result
