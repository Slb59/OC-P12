from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey,
    Column, Integer, String, TIMESTAMP
    )
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType
from sqlalchemy.exc import NoResultFound

Base = declarative_base()


class DateFields():
    """ a common class for timestamping """
    created_on = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_on = Column(TIMESTAMP, onupdate=func.now())
    # created_by_id = Column(Integer, ForeignKey('employees.id'))
    # created_by = relationship('Employee', back_populates='creators')
    # updated_by = Column(Integer, ForeignKey('employees.id'))

    class Meta:
        abstract = True


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    employees = relationship('Employee', back_populates='department')

    def __repr__(self):
        return f'{self.name}'

    @classmethod
    def getall(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).one()


class Employee(Base):
    __tablename__ = 'employees'

    EMPLOYEE_STATES = (
        ('A', 'Actif'),
        ('I', 'Inactif')
    )

    EMPLOYEE_ROLES = (
        ('C', 'Commercial'),
        ('M', 'Manager'),
        ('S', 'Support')
    )

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String)
    password = Column(String)
    role = Column(
        ChoiceType(EMPLOYEE_ROLES, impl=String(length=1)),
        nullable=False)
    state = Column(
        ChoiceType(EMPLOYEE_STATES, impl=String(length=1)), default='A'
        )

    department_id = Column(
        Integer, ForeignKey('departments.id'), nullable=False
        )
    department = relationship('Department', back_populates='employees')

    tasks = relationship('Task', back_populates='employee')

    class Meta:
        abstract = True

    # def __init__(self, username, department_id, email, password, role):
    #     self.username = username
    #     self.depatment_id = department_id
    #     self.email = email
    #     self.password = password
    #     self.role = role

    def __repr__(self):
        if self.state == 'A':
            s = f'username: {self.username}\n'
            s += f'email: {self.email}\n'
            s += f'department: {self.department}'
        else:
            s = f'Employee n°{self.id} is inactivate'
        return s

    def __str__(self) -> str:
        if self.state == 'A':
            return f'{self.username}'
        else:
            return f'Employee n°{self.id} is inactivate'

    def __eq__(self, e) -> bool:
        return self.username == e.username

    def to_dict(self) -> dict:
        return {
                'username': self.username,
                'password': self.password,
                'email': self.email,
                'role': self.role.value,
                'state': self.state.value
            }

    @classmethod
    def find_by_userpwd(cls, session, username, password):
        try:
            return session.query(cls).filter_by(
                username=username, password=password).one()
        except NoResultFound:
            return None

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).one()

    @classmethod
    def find_by_department(cls, session, department_id):
        return session.query(cls).filter_by(department_id=department_id).all()

    def update_role(self, new_role):
        self.role = new_role


class ContractsAreActived(Exception):
    def __init__(self, message="Some contracts are actived"):
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return 'Some contracts are actived'


class Commercial(Employee):

    clients = relationship('Client', back_populates='commercial')

    @property
    def contracts(self):
        contracts = []
        for c in self.clients:
            contracts.extend(c.contracts)
        return contracts

    # def __init__(self, username, department_id, email='', password=''):
    #     super().__init__(username, department_id, email, password, 'C')

    def update_role(self, new_role):
        # check all contracts are balanced
        all_contracts_balanced = True
        for c in self.contracts:
            if c.state != 'X' and c.state != 'B':
                all_contracts_balanced = False
        if all_contracts_balanced:
            self.role = new_role
        else:
            raise ContractsAreActived()


class Support(Employee):

    events = relationship('Event', back_populates='support')


class Manager(Employee):
    ...


class Task(Base):
    __tablename__ = 'tasks'

    TASK_STATES = (
        ('T', 'Todo'),
        ('D', 'Done')
    )

    id = Column(Integer, primary_key=True)
    description = Column(String)
    started_time = Column(TIMESTAMP, nullable=False, default=datetime.now())
    ended_time = Column(TIMESTAMP)
    state = Column(
        ChoiceType(TASK_STATES, impl=String(length=1)), default='T'
        )

    employee_id = Column(
        Integer, ForeignKey('employees.id'), nullable=False
        )
    employee = relationship('Employee', back_populates='tasks')

    def __repr__(self):
        return f'Task {self.description}'


class Client(Base, DateFields):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False, unique=True)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    commercial_id = Column(Integer, ForeignKey('employees.id'))
    commercial = relationship('Commercial', back_populates='clients')

    contracts = relationship('Contract', back_populates='client')

    def __repr__(self):
        return f'Client {self.full_name}'

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(full_name=name).one()

    @classmethod
    def getall(cls, session):
        return session.query(cls).all()

    @property
    def actif_contracts(self):
        actifs = []
        for c in self.contracts:
            if c.state in ['C', 'S']:
                actifs.append(c)
        return actifs


class Contract(Base, DateFields):
    __tablename__ = 'contracts'

    CONTRACT_STATES = (
        ('C', 'Créé'),
        ('S', 'Signé'),
        ('B', 'Soldé'),
        ('X', 'Annulé')
    )

    id = Column(Integer, primary_key=True)
    ref = Column(String, nullable=False, unique=True)
    description = Column(String)
    total_amount = Column(Integer, nullable=False)
    state = Column(
        ChoiceType(CONTRACT_STATES, impl=String(length=1)), default='C'
        )

    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='contracts')

    paiements = relationship('Paiement', back_populates='contract')
    events = relationship('Event', back_populates='contract')

    def __repr__(self):
        return f'{self.description}'

    @classmethod
    def find_by_ref(cls, session, ref):
        return session.query(cls).filter_by(ref=ref).one()

    @classmethod
    def getall(cls, session):
        return session.query(cls).all()

    @property
    def outstanding(self):
        total_paiements = 0
        for p in self.paiements:
            total_paiements += p.amount
        return self.total_amount - total_paiements


class Paiement(Base):
    __tablename__ = 'paiements'
    id = Column(Integer, primary_key=True)
    ref = Column(String, nullable=False, unique=True)
    date_amount = Column(TIMESTAMP, nullable=False, default=datetime.now())
    amount = Column(Integer)

    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship('Contract', back_populates='paiements')

    def __repr__(self):
        return f'{self.date_amount}: {self.ref}/{self.amount}'


class EventType(Base):
    __tablename__ = 'eventstype'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)

    events = relationship('Event', back_populates='type')

    def __repr__(self):
        return f'{self.title}'

    @classmethod
    def find_by_title(cls, session, title):
        return session.query(cls).filter_by(title=title).one()


class Event(Base):
    __tablename__ = 'events'

    EVENT_STATES = (
        ('U', 'Upcoming'),
        ('C', 'Completed'),
        ('X', 'Canceled')
    )

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String)
    attendees = Column(Integer)
    report = Column(String)
    date_started = Column(TIMESTAMP, nullable=False)
    date_ended = Column(TIMESTAMP, nullable=False)
    state = Column(
        ChoiceType(EVENT_STATES, impl=String(length=1)), default='U'
        )

    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship('Contract', back_populates='events')

    type_id = Column(Integer, ForeignKey('eventstype.id'))
    type = relationship('EventType', back_populates='events')

    support_id = Column(Integer, ForeignKey('employees.id'))
    support = relationship('Support', back_populates='events')

    def __repr__(self):
        return f'{self.title}'

    @classmethod
    def find_by_title(cls, session, title):
        return session.query(cls).filter_by(title=title).one()
