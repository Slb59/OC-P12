from epicevents.models.entities import Department, Employee


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

    def test_list_departments(self, db_session):
        """
        count list of department is 3
        and the first one is management department
        """
        self.initdb(db_session)
        assert db_session.query(Department).count() == 3
        departments = Department.getall(db_session)
        assert departments[0].name == 'management department'

    def test_list_employee_department(self, db_session):
        """
        count list of employees in department 3
        """
        self.initdb(db_session)
        self.add_commercials(db_session)
        d3 = db_session.query(Department).all()[2]
        assert len(d3.getemployees(db_session)) == 3
