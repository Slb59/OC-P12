import pytest
from sqlalchemy.exc import IntegrityError
from epicevents.models.entities import Department, Employee, Task


class TestEmployees:

    def initdb(self, db_session):
        management_dpt = Department(name='management department')
        support_dpt = Department(name='support department')
        commercial_dpt = Department(name='commercial department')
        db_session.add_all([management_dpt, support_dpt, commercial_dpt])

    def add_commercials(self, db_session):
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Employee(username='Yuka', department_id=d.id)
        e2 = Employee(username='Esumi', department_id=d.id)
        e3 = Employee(username='Morihei', department_id=d.id)
        db_session.add_all([e1, e2, e3])

    def add_yuka(self, db_session):
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Employee(username='Yuka', department_id=d.id)
        db_session.add(e1)

    def add_tasks_on_yuka(self, db_session):
        e = Employee.find_by_username(db_session, 'Yuka')
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

    def test_list_departments(self, db_session):
        """
        count list of department is 3
        and the first one is management department
        """
        self.initdb(db_session)
        assert db_session.query(Department).count() == 3
        departments = Department.getall(db_session)
        assert departments[0].name == 'management department'

    def test_repr_employee(self, db_session):
        self.initdb(db_session)
        d = Department.find_by_name(db_session, 'commercial department')
        e = Employee(username='Yuka', department_id=d.id)
        e.email = 'Yuka@example.com'
        db_session.add(e)
        e = Employee.find_by_username(db_session, 'Yuka')
        result = 'username: Yuka\nemail: Yuka@example.com\n'\
            + 'department: commercial department'
        assert repr(e) == result
        e.state = 'I'
        assert repr(e) == 'Employee n°1 is inactivate'

    def test_list_employee_department(self, db_session):
        """
        count list of employees in department 3
        """
        self.initdb(db_session)
        self.add_commercials(db_session)
        d3 = db_session.query(Department).all()[2]
        assert len(d3.employees) == 3

    def test_list_employee_tasks(self, db_session):
        self.initdb(db_session)
        self.add_yuka(db_session)
        self.add_tasks_on_yuka(db_session)
        e = Employee.find_by_username(db_session, 'Yuka')
        assert len(e.tasks) == 3

    @pytest.mark.xfail(raises=IntegrityError)
    def test_department_unique_name(self, db_session):
        newdpt = Department(name='management department')
        db_session.add(newdpt)
        try:
            db_session.commit()
        except IntegrityError:
            db_session.rollback()
