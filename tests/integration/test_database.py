from sqlalchemy_utils import drop_database
from epicevents.controllers.database import EpicDatabase
from epicevents.models.entities import (
    Manager, Department, Commercial, Employee,
    Client, Contract, EventType, Event)


def init_test_get_clients():
    # given
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    e2 = Commercial(username='Esumi', department_id=d.id, role='C')
    db.session.add_all([e1, e2])
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    c1 = Client(full_name='c1', commercial_id=e1.id)
    e2 = Commercial.find_by_username(db.session, 'Esumi')
    c2 = Client(full_name='c2', commercial_id=e2.id)
    db.session.add_all([c1, c2])
    return db


def test_init_database():
    db = EpicDatabase("epictest2", "localhost", "postgres", "postgres", "5432")
    assert str(db) == 'epictest2 database'


def test_database_creation():
    db = EpicDatabase("epictest2", "localhost", "postgres", "postgres", "5432")
    drop_database(db.url)
    db = EpicDatabase("epictest2", "localhost", "postgres", "postgres", "5432")
    assert str(db) == 'epictest2 database'


def test_check_connection():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.dbemployees.add_employee('Misoka', 'Misoka', 'Manager')
    e_base = Manager.find_by_username(db.session, 'Misoka')
    e_result = db.check_connection('Misoka', 'Misoka')
    db.session.close()
    assert e_base == e_result


def test_check_connection_error():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.dbemployees.add_employee('Misoka2', 'Misoka', 'Manager')
    e_result = db.check_connection('Misoka2', 'Misoka2')
    db.session.close()
    assert e_result is None


def test_check_employee():
    # given
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    d = Department.find_by_name(db.session, 'management department')
    e = Manager(username='Yuka', department_id=d.id, role='C')
    db.session.add(e)
    # when
    result = db.check_employee('Yuka')
    # then
    db.session.close()
    assert result == e


def test_get_events():
    # given
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    drop_database(db.url)
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    e2 = Employee(username='Aritomo', department_id=d.id, role='S')
    db.session.add_all([e1, e2])
    e = Commercial.find_by_username(db.session, 'Yuka')
    c = Client(full_name='c1', commercial_id=e.id)
    db.session.add(c)
    c = Client.find_by_name(db.session, 'c1')
    contract = Contract(
        ref='ref1', client_id=c.id, description='desc', total_amount=10)
    db.session.add(contract)
    t = EventType.find_by_title(db.session, 'seminar')
    contract = Contract.find_by_ref(db.session, 'ref1')
    e = Employee.find_by_username(db.session, 'Aritomo')
    e1 = Event(
        title='title 1',
        contract_id=contract.id,
        date_started='2023-09-14 15:00:00.000000',
        date_ended='2023-09-24 18:00:00.000000',
        type_id=t.id,
        support_id=e.id)
    e2 = Event(
        title='title 2',
        contract_id=contract.id,
        date_started='2023-09-14 09:00:00.000000',
        date_ended='2023-09-14 18:00:00.000000',
        type_id=t.id)
    db.session.add_all([e1, e2])
    # when
    result = Event.getall(db.session)
    assert len(result) == 2
    result = db.get_events()
    # then
    assert len(result) == 2
    db.session.close()
