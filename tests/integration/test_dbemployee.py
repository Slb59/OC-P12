from epicevents.controllers.database import EpicDatabase
from epicevents.models.entities import Employee


def test_add_employees():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.dbemployees.add_employee('Misoka', 'Misoka', 'Manager')
    db.dbemployees.add_employee('Yuka', 'Yuka', 'Commercial')
    db.dbemployees.add_employee('Aritomo', 'Aritomo', 'Support')
    result = Employee.getall(db.session)
    assert len(result) == 4
    for e in result:
        db.session.delete(e)
    db.session.commit()
    db.session.close()


def test_get_employees():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.dbemployees.add_employee('Osy', 'Osy', 'Manager')
    result = db.dbemployees.get_employees()
    assert len(result) == 1
    db.session.close()


def test_get_roles():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    list = ['Commercial', 'Manager', 'Support']
    result = db.dbemployees.get_roles()
    assert list == result
    db.session.close()
