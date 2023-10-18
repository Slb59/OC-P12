import pytest
from epicevents.models.entities import (
    Department, Commercial, Client, EventType)


@pytest.fixture()
def commercial_department(db_session):
    name = 'commercial department'
    dpt = Department(name=name)
    db_session.add(dpt)
    return name


@pytest.fixture()
def support_department(db_session):
    name = 'support department'
    dpt = Department(name=name)
    db_session.add(dpt)
    return name


@pytest.fixture()
def management_department(db_session):
    name = 'management department'
    dpt = Department(name=name)
    db_session.add(dpt)
    return name


@pytest.fixture()
def yuka(db_session, commercial_department):
    d = Department.find_by_name(db_session, commercial_department)
    e = Commercial(
        username='Yuka', password='Yuka', department_id=d.id, role='C')
    db_session.add(e)
    return 'Yuka'


@pytest.fixture()
def add_3_commercials(db_session, commercial_department):
    d = Department.find_by_name(db_session, commercial_department)
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    e2 = Commercial(username='Esumi', department_id=d.id, role='C')
    e3 = Commercial(username='Morihei', department_id=d.id, role='C')
    db_session.add_all([e1, e2, e3])


@pytest.fixture()
def add_3_clients_to_yuka(db_session):
    e = Commercial.find_by_username(db_session, 'Yuka')
    c1 = Client(full_name='Client 1', commercial_id=e.id)
    c2 = Client(full_name='Client 2', commercial_id=e.id)
    c3 = Client(full_name='Client 3', commercial_id=e.id)
    db_session.add_all([c1, c2, c3])


@pytest.fixture()
def event_types(db_session):
    event_type1 = EventType(title='conference')
    event_type2 = EventType(title='forum')
    event_type3 = EventType(title='show')
    event_type4 = EventType(title='seminar')
    list_events = [event_type1, event_type2, event_type3, event_type4]
    db_session.add_all(list_events)
    return list_events
