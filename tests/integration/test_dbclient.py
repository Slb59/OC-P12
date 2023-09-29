import logging
from epicevents.models.entities import (
    Department, Commercial, Client
)

log = logging.getLogger()


def init_test_get_clients(db):
    # given
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    e2 = Commercial(username='Esumi', department_id=d.id, role='C')
    db.session.add_all([e1, e2])
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    c1 = Client(full_name='c1', commercial_id=e1.id)
    e2 = Commercial.find_by_username(db.session, 'Esumi')
    c2 = Client(full_name='c2', commercial_id=e2.id)
    db.session.add_all([c1, c2])


def delete_init(db):
    c1 = Client.find_by_name(db.session, 'c1')
    db.session.delete(c1)
    c2 = Client.find_by_name(db.session, 'c2')
    db.session.delete(c2)
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    db.session.delete(e1)
    e2 = Commercial.find_by_username(db.session, 'Esumi')
    db.session.delete(e2)
    db.session.commit()


def test_get_clients_without_name(epictest2):
    # given
    db = epictest2
    init_test_get_clients(db)
    c1 = Client.find_by_name(db.session, 'c1')
    c2 = Client.find_by_name(db.session, 'c2')
    # when
    result = db.dbclients.get_clients()
    # then
    assert result == [c1, c2]


def test_get_clients_with_name(epictest2):
    # given
    db = epictest2
    init_test_get_clients(db)
    c1 = Client.find_by_name(db.session, 'c1')
    c2 = Client.find_by_name(db.session, 'c2')
    # when
    result = db.dbclients.get_clients('Yuka')
    # then
    assert c1 in result
    assert c2 not in result


def test_update_commercial(epictest2):
    db = epictest2
    init_test_get_clients(db)
    db.dbclients.update_commercial('c1', 'Esumi')
    c = Client.find_by_name(db.session, 'c1')
    assert c.commercial.username == 'Esumi'
    delete_init(db)


def test_create_client(epictest2):
    # given
    db = epictest2
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    db.session.add(e1)
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    data = {
        'full_name': 'client-test', 'email': 'test@test.com',
        'phone': '0202020202', 'company_name': 'company_name'}
    # when
    db.dbclients.create(e1.username, data)
    c = Client.find_by_name(db.session, 'client-test')
    # then
    db.session.delete(c)
    db.session.delete(e1)
    db.session.commit()
    assert c.full_name == 'client-test'
    log.debug(c)
    log.debug(c.commercial_id)
    assert c.commercial.username == 'Yuka'


def test_update(epictest2):
    db = epictest2
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    db.session.add(e1)
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    c = Client(full_name='test', commercial_id=e1.id)
    db.session.add(c)
    data = {
        'full_name': 'client-test', 'email': 'test@test.com',
        'phone': '0202020202', 'company_name': 'company_name'}
    db.dbclients.update('test', data)
    c = Client.find_by_name(db.session, 'client-test')
    db.session.delete(c)
    db.session.delete(e1)
    db.session.commit()
    assert c.email == 'test@test.com'

