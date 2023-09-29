import logging
from epicevents.models.entities import (
    Department, Commercial, Client, Employee,
    Contract, EventType, Event
)

log = logging.getLogger()


def initdb(db):
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


def deletedb(db):
    contract = Contract.find_by_ref(db.session, 'ref1')
    e = Event.find_by_title(db.session, contract.id, 'title 2')
    db.session.delete(e)
    e = Event.find_by_title(db.session, contract.id, 'title 1')
    db.session.delete(e)
    db.session.delete(contract)
    c = Client.find_by_name(db.session, 'c1')
    db.session.delete(c)
    e = Commercial.find_by_username(db.session, 'Yuka')
    db.session.delete(e)
    e = Commercial.find_by_username(db.session, 'Aritomo')
    db.session.delete(e)
    db.session.commit()


def test_get_events(epictest2):
    # given
    db = epictest2
    initdb(db)
    # when
    result = Event.getall(db.session)
    assert len(result) == 2
    log.debug(result)
    assert len(result) == 2
    result = db.dbevents.get_events(None, None, None, None)
    # then
    assert len(result) == 2
    sname = '-- sans support --'
    result = db.dbevents.get_events(None, None, None, sname)
    assert len(result) == 1


def test_update(epictest2):
    # given
    db = epictest2
    initdb(db)
    # when
    c = Contract.find_by_ref(db.session, 'ref1')
    e = Event.find_by_title(db.session, c.id, 'title 2')
    assert e.support is None
    db.dbevents.update('ref1', 'title 2', 'Aritomo')
    # then
    e = Event.find_by_title(db.session, c.id, 'title 2')
    assert e.support.username == 'Aritomo'
    deletedb(db)


def test_get_types(epictest2):
    db = epictest2
    result = db.dbevents.get_types()
    result = [r.title for r in result]
    expected = ['conference', 'forum', 'show', 'seminar']
    assert expected == result
