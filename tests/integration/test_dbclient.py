from epicevents.controllers.database import EpicDatabase
from epicevents.models.entities import (
    Department, Commercial, Client
)


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
    result = db.dbclients.get_clients()
    # then
    db.session.close()
    assert result == [c1, c2]


def test_get_clients_with_name():
    # given
    db = init_test_get_clients()
    c1 = Client.find_by_name(db.session, 'c1')
    c2 = Client.find_by_name(db.session, 'c2')
    # when
    result = db.dbclients.get_clients('Yuka')
    # then
    db.session.close()
    assert c1 in result
    assert c2 not in result
