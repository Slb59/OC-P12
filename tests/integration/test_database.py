from sqlalchemy_utils import drop_database
from epicevents.controllers.database import EpicDatabase
from epicevents.models.entities import (
    Manager, Department, Commercial,
    Client)


def test_init_database():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    drop_database(db.url)
    assert str(db) == 'epictest2 database'


def test_check_connection():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.add_employee('Misoka', 'Misoka', 'Manager')
    e_base = Manager.find_by_username(db.session, 'Misoka')
    e_result = db.check_connection('Misoka', 'Misoka')
    db.session.close()
    drop_database(db.url)
    assert e_base == e_result


def test_check_connection_error():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.add_employee('Misoka', 'Misoka', 'Manager')
    e_result = db.check_connection('Misoka', 'Misoka2')
    db.session.close()
    drop_database(db.url)
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
    drop_database(db.url)
    assert result == e


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


def test_get_clients_without_name():
    # given
    db = init_test_get_clients()
    c1 = Client.find_by_name(db.session, 'c1')
    c2 = Client.find_by_name(db.session, 'c2')
    # when
    result = db.get_clients()
    # then
    db.session.close()
    drop_database(db.url)    
    assert result == [c1, c2]


def test_get_clients_with_name():
    # given
    db = init_test_get_clients()
    c1 = Client.find_by_name(db.session, 'c1')
    c2 = Client.find_by_name(db.session, 'c2')
    # when
    result = db.get_clients('Yuka')
    # then
    db.session.close()
    drop_database(db.url)
    assert c1 in result
    assert c2 not in result
