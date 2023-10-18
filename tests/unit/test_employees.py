import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from epicevents.models.entities import (
    Department, Employee, Commercial, Task, Manager
)


def add_managers(db_session):
    d = Department.find_by_name(db_session, 'management department')
    e1 = Manager(username='Osynia', department_id=d.id, role='M')
    e2 = Manager(username='Misoka', department_id=d.id, role='M')
    db_session.add_all([e1, e2])


def add_tasks_on_yuka(db_session):
    e = Commercial.find_by_username(db_session, 'Yuka')
    t1 = Task(
        description='Create events for client 1 contrat 2023091401',
        employee_id=e.id)
    t2 = Task(
        description='another job todo',
        employee_id=e.id)
    t3 = Task(
        description='and another job one',
        employee_id=e.id)
    db_session.add_all([t1, t2, t3])


class TestEmployees:

    def test_list_departments(
            self, db_session,
            commercial_department,
            support_department,
            management_department):
        """
        count list of department is 3
        and the first one is management department
        """
        # GIVEN there is 3 departmenet in database
        # then
        assert db_session.query(Department).count() == 3
        departments = Department.getall(db_session)
        assert departments[2].name == management_department

    def test_repr_employee(self, db_session, commercial_department):
        # GIVEN there is a commercial department
        d = Department.find_by_name(db_session, commercial_department)
        e = Commercial(username='Yuka', department_id=d.id, role='C')
        e.email = 'Yuka@example.com'
        db_session.add(e)
        # when
        e = Commercial.find_by_username(db_session, 'Yuka')
        # then
        result = 'username: Yuka\nemail: Yuka@example.com\n'\
            + 'department: commercial department'
        assert repr(e) == result
        e.state = 'I'
        assert repr(e) == f'Employee n°{e.id} is inactivate'

    def test_to_dict(self, db_session, commercial_department):
        # GIVEN database has a commercial department
        d = Department.find_by_name(db_session, commercial_department)
        result = {
            'username': 'Yuka',
            'password': 'Yuka',
            'email': 'yuka@example.com',
            'role': 'Commercial',
            'state': 'Actif'
        }
        e = Commercial(
            username='Yuka', password='Yuka',
            email='yuka@example.com', department_id=d.id, role='C')
        db_session.add(e)
        e = Employee.find_by_username(db_session, 'Yuka')
        assert result == e.to_dict()

    def test_getall(
            self, db_session, add_3_commercials):
        # GIVEN database has a commercial department
        # GiVEN database has 3 commercials
        e1 = Employee.find_by_username(db_session, 'Yuka')
        e2 = Employee.find_by_username(db_session, 'Esumi')
        e3 = Employee.find_by_username(db_session, 'Morihei')
        result = [e2, e3, e1]
        employees = Employee.getall(db_session)
        assert result == employees

    def test_list_employee_department(self, db_session, add_3_commercials):
        """
        count list of employees in department commercial
        """
        # GIVEN database has a commercial department
        # GiVEN database has 3 commercials
        # WHEN
        d = db_session.query(Department).all()[0]
        # then
        assert len(d.employees) == 3

    def test_list_employee_tasks(self, db_session, yuka):
        # GIVEN database has a commercial department
        # GIVEN database has yuka as commercial
        # when
        add_tasks_on_yuka(db_session)
        e = Commercial.find_by_username(db_session, yuka)
        # then
        assert len(e.tasks) == 3

    def test_find_by_userpwd(self, db_session, yuka):
        # GIVEN database has a commercial department
        # GIVEN database has yuka as commercial
        e = Employee.find_by_username(db_session, yuka)
        result = Employee.find_by_userpwd(db_session, 'Yuka', 'Yuka')
        assert e == result

    def test_find_by_department(self, db_session, add_3_commercials):
        # GIVEN database has a commercial department
        # GIVEN database has 3 commercials
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Employee.find_by_username(db_session, 'Yuka')
        e2 = Employee.find_by_username(db_session, 'Esumi')
        e3 = Employee.find_by_username(db_session, 'Morihei')
        result = [e1, e2, e3]
        employees = Employee.find_by_department(db_session, d.id)
        assert employees == result

    def test_getall_commercials(
            self, db_session, add_3_commercials, management_department):
        # GIVEN database has a commercial department
        # GIVEN database has 3 commercials
        # GIVEN database has a management department
        add_managers(db_session)
        e1 = Employee.find_by_username(db_session, 'Yuka')
        e2 = Employee.find_by_username(db_session, 'Esumi')
        e3 = Employee.find_by_username(db_session, 'Morihei')
        e4 = Employee.find_by_username(db_session, 'Osynia')
        result = [e2, e3, e1]
        commercials = Commercial.getall(db_session)
        assert result == commercials
        assert e4 not in commercials


class TestTask:

    def test_repr_task(self, db_session, yuka):
        # GIVEN database has a commercial department
        # GIVEN yuka is a employee of commercial department
        e = Employee.find_by_username(db_session, yuka)
        # when
        t = Task(description='ma description', employee_id=e.id)
        db_session.add(t)
        t = db_session.query(Task).first()
        # then
        fmt = '%d/%m/%Y'
        assert repr(t) == f'{datetime.now().strftime(fmt)}:ma description'


class TestEmployeeUnique:

    def test_department_unique_name(self, db_session, management_department):
        # GIVEN database has a management department
        # when
        newdpt = Department(name='management department')
        with pytest.raises(IntegrityError) as e_info:
            db_session.add(newdpt)
            db_session.commit()
        # then except IntegrityError
        assert e_info.type is IntegrityError

    def test_employee_unique_name(
            self, db_session, commercial_department, yuka):
        # GIVEN database has a commercial department
        # GIVEN yuka is employee od commercial department
        d = Department.find_by_name(db_session, commercial_department)
        # when
        e2 = Commercial(username=yuka, department_id=d.id, role='C')
        with pytest.raises(IntegrityError) as e_info:
            db_session.add(e2)
            db_session.commit()
        # then except IntegrityError
        assert e_info.type is IntegrityError
