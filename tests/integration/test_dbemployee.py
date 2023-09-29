import logging
from epicevents.models.entities import Employee

log = logging.getLogger()


def test_add_employees(epictest2):
    db = epictest2
    db.dbemployees.add_employee('MisokaX', 'Misoka', 'Manager')
    db.dbemployees.add_employee('YukaX', 'Yuka', 'Commercial')
    db.dbemployees.add_employee('AritomoX', 'Aritomo', 'Support')
    result = Employee.getall(db.session)
    assert len(result) == 4
    for e in result:
        if e.username != 'Osynia':
            db.session.delete(e)
    db.session.commit()


def test_get_employees(epictest2):
    db = epictest2
    db.dbemployees.add_employee('Osy', 'Osy', 'Manager')
    result = db.dbemployees.get_employees()
    log.debug(result)
    assert len(result) == 2
    e = Employee.find_by_username(db.session, 'Osy')
    db.session.delete(e)
    db.session.commit()


def test_get_roles(epictest2):
    db = epictest2
    list = ['Commercial', 'Manager', 'Support']
    result = db.dbemployees.get_roles()
    assert list == result
