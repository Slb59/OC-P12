# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, server_default=text("nextval('departments_id_seq'::regclass)"))
    name = Column(String, nullable=False, unique=True)


class Eventstype(Base):
    __tablename__ = 'eventstype'

    id = Column(Integer, primary_key=True, server_default=text("nextval('eventstype_id_seq'::regclass)"))
    title = Column(String, nullable=False, unique=True)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, server_default=text("nextval('employees_id_seq'::regclass)"))
    username = Column(String, nullable=False, unique=True)
    email = Column(String)
    password = Column(String)
    role = Column(String(1), nullable=False)
    state = Column(String(1))
    department_id = Column(ForeignKey('departments.id'), nullable=False)

    department = relationship('Department')


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, server_default=text("nextval('clients_id_seq'::regclass)"))
    full_name = Column(String, nullable=False, unique=True)
    email = Column(String)
    phone = Column(String)
    company_name = Column(String)
    commercial_id = Column(ForeignKey('employees.id'))
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime)

    commercial = relationship('Employee')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, server_default=text("nextval('tasks_id_seq'::regclass)"))
    description = Column(String)
    started_time = Column(DateTime, nullable=False)
    ended_time = Column(DateTime)
    state = Column(String(1))
    employee_id = Column(ForeignKey('employees.id'), nullable=False)

    employee = relationship('Employee')


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, server_default=text("nextval('contracts_id_seq'::regclass)"))
    ref = Column(String, nullable=False, unique=True)
    description = Column(String)
    total_amount = Column(Integer, nullable=False)
    state = Column(String(1))
    client_id = Column(ForeignKey('clients.id'))
    created_on = Column(DateTime, nullable=False)
    updated_on = Column(DateTime)

    client = relationship('Client')


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, server_default=text("nextval('events_id_seq'::regclass)"))
    title = Column(String, nullable=False)
    description = Column(String)
    location = Column(String)
    attendees = Column(Integer)
    report = Column(String)
    date_started = Column(DateTime, nullable=False)
    date_ended = Column(DateTime, nullable=False)
    state = Column(String(1))
    contract_id = Column(ForeignKey('contracts.id'))
    type_id = Column(ForeignKey('eventstype.id'))
    support_id = Column(ForeignKey('employees.id'))

    contract = relationship('Contract')
    support = relationship('Employee')
    type = relationship('Eventstype')


class Paiement(Base):
    __tablename__ = 'paiements'

    id = Column(Integer, primary_key=True, server_default=text("nextval('paiements_id_seq'::regclass)"))
    ref = Column(String, nullable=False, unique=True)
    date_amount = Column(DateTime, nullable=False)
    amount = Column(Integer)
    contract_id = Column(ForeignKey('contracts.id'))

    contract = relationship('Contract')
