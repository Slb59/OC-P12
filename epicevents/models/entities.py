from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    ForeignKey,
    Column, Integer, String, TIMESTAMP
    )
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import ChoiceType

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
    name = Column(String)
    employees = relationship('Employee', back_populates='department')

    def __repr__(self):
        return f'Department {self.name}'


class Employee(Base):
    __tablename__ = 'employees'

    EMPLOYEE_STATES = (
        ('A', 'Actif'),
        ('I', 'Inactif')
    )

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    state = Column(
        ChoiceType(EMPLOYEE_STATES, impl=String(length=1)), default='A'
        )

    department_id = Column(
        Integer, ForeignKey('departments.id'), nullable=False
        )
    department = relationship('Department', back_populates='employees')

    clients = relationship('Client', back_populates='commercial')
    tasks = relationship('Task', back_populates='employee')

    def __repr__(self):
        return f'User {self.name}'

    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).all()

    @classmethod
    def find_by_departmentname(cls, session, departmentname):
        return None


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
    full_name = Column(String)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    commercial_id = Column(Integer, ForeignKey('employees.id'))
    commercial = relationship('Employee', back_populates='clients')

    contracts = relationship('Contract', back_populates='client')

    def __repr__(self):
        return f'Client {self.full_name}'


class Contract(Base, DateFields):
    __tablename__ = 'contracts'

    CONTRACT_STATES = (
        ('C', 'Created'),
        ('S', 'signed'),
        ('B', 'balanced')
    )

    id = Column(Integer, primary_key=True)
    description = Column(String)
    total_amount = Column(Integer)
    state = Column(
        ChoiceType(CONTRACT_STATES, impl=String(length=1)), default='C'
        )

    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='contracts')

    def __repr__(self):
        return f'Contract {self.description}'
