import logging
from sqlalchemy.exc import NoResultFound
from epicevents.views.console import console
from epicevents.models.entities import (
    Department, Commercial, Client, Contract, Paiement)


log = logging.getLogger()


def initdb(db):
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    db.session.add(e1)
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    c = Client(full_name='c1', commercial_id=e1.id)
    db.session.add(c)
    c = Client.find_by_name(db.session, 'c1')
    c1 = Contract(
        ref='ref1', description='desc1', total_amount=10000, client_id=c.id)
    c2 = Contract(
        ref='ref2', description='desc2', total_amount=1000, client_id=c.id)
    db.session.add_all([c1, c2])


def deletedb(db):
    try:
        c1 = Contract.find_by_ref(db.session, 'ref1')
        db.session.delete(c1)
    except NoResultFound:
        pass
    c2 = Contract.find_by_ref(db.session, 'ref2')
    db.session.delete(c2)
    c = Client.find_by_name(db.session, 'c1')
    db.session.delete(c)
    e = Commercial.find_by_username(db.session, 'Yuka')
    db.session.delete(e)


def test_get_states(epictest2):
    db = epictest2
    result = db.dbcontracts.get_states()
    expected = ['Créé', 'Signé', 'Soldé', 'Annulé']
    assert result == expected


def test_get_state(epictest2):
    db = epictest2
    initdb(db)
    result = db.dbcontracts.get_state('ref1')
    assert result == 'C'


def test_get_contracts(epictest2):
    db = epictest2
    initdb(db)
    result = db.dbcontracts.get_contracts()
    log.debug(result)
    assert len(result) == 2
    result = db.dbcontracts.get_contracts(commercial_name='Yuka')
    assert len(result) == 2


def test_get_active_contracts(epictest2):
    db = epictest2
    initdb(db)
    result = db.dbcontracts.get_active_contracts()
    assert len(result) == 2


def test_create(epictest2):
    db = epictest2
    initdb(db)
    data = {
        'ref': 'testcreate',
        'description': 'testcreate',
        'total_amount': '10000'}
    db.dbcontracts.create('c1', data)
    c = Contract.find_by_ref(db.session, 'testcreate')
    assert c.ref == 'testcreate'
    db.session.delete(c)
    deletedb(db)
    db.session.commit()


def test_add_paiement(epictest2):
    db = epictest2
    initdb(db)
    data = {
        'ref': 'testpaiement',
        'amount': '1000'}
    db.dbcontracts.add_paiement('ref1', data)
    c = Contract.find_by_ref(db.session, 'ref1')
    assert c.outstanding == 9000
    data = {
        'ref': 'testpaiement2',
        'amount': '10000'}
    with console.capture() as capture:
        db.dbcontracts.add_paiement('ref1', data)
    output = capture.get()
    assert c.outstanding == 9000
    assert output == 'Ce montant est supérieur au restant dû\n'
    p = Paiement.find_by_ref(db.session, 'testpaiement')
    db.session.delete(p)
    deletedb(db)
    db.session.commit()


def test_update(epictest2):
    db = epictest2
    initdb(db)
    data = {
        'ref': 'newref',
        'description': 'new description',
        'total_amount': '20000'}
    db.dbcontracts.update('ref1', data)
    c = Contract.find_by_ref(db.session, 'newref')
    assert c.total_amount == 20000
    db.session.delete(c)
    deletedb(db)
    db.session.commit()
