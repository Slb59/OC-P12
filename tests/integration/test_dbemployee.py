import logging
from epicevents.models.entities import Department, Employee, Task

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


def test_get_managers(epictest2):
    db = epictest2
    d = Department.getall(db.session)
    e = Employee(username='Emp2', department_id=d[0].id, role='M')
    db.session.add(e)
    managers = db.dbemployees.get_managers()
    log.debug(managers)
    assert len(managers) == 2


def test_get_commercials(epictest2):
    db = epictest2
    d = Department.getall(db.session)
    e1 = Employee(username='Emp2', department_id=d[0].id, role='C')
    e2 = Employee(username='Emp3', department_id=d[0].id, role='C')
    db.session.add_all([e1, e2])
    result = db.dbemployees.get_commercials()
    assert len(result) == 2


def test_get_supports(epictest2):
    db = epictest2
    d = Department.getall(db.session)
    e1 = Employee(username='Emp2', department_id=d[0].id, role='S')
    e2 = Employee(username='Emp3', department_id=d[0].id, role='S')
    db.session.add_all([e1, e2])
    result = db.dbemployees.get_supports()
    assert len(result) == 2


def test_get_rolecode(epictest2):
    db = epictest2
    result = db.dbemployees.get_rolecode('Manager')
    assert result == 'M'


def test_get_tasks(epictest2):
    db = epictest2
    e = Employee.find_by_username(db.session, 'Osynia')
    t1 = Task(description='une tache', employee_id=e.id)
    t2 = Task(description='une tache', employee_id=e.id)
    db.session.add_all([t1, t2])
    result = db.dbemployees.get_tasks(e)
    assert len(result) == 2
