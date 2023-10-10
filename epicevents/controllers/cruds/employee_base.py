from argon2 import PasswordHasher
from sqlalchemy.exc import IntegrityError
from epicevents.views.data_views import DataView
from epicevents.views.business_views.event_views import EventView
from epicevents.models.entities import (
    Department, Manager, Commercial, Support,
    Employee, Task
)


class EmployeeBase:

    """ Manage crud operations on Employee base """

    def __init__(self, session) -> None:
        self.ph = PasswordHasher()
        self.session = session

    def add_employee(self, username, password, role):

        hashed_password = self.ph.hash(password)

        match role:
            case 'Manager':
                d = Department.find_by_name(
                    self.session, 'management department')
                e = Manager(
                    username=username,
                    password=hashed_password,
                    department_id=d.id,
                    role='M')
            case 'Commercial':
                d = Department.find_by_name(
                    self.session, 'commercial department')
                e = Commercial(
                    username=username,
                    password=hashed_password,
                    department_id=d.id,
                    role='C')
            case 'Support':
                d = Department.find_by_name(
                    self.session, 'support department')
                e = Support(
                    username=username,
                    password=hashed_password,
                    department_id=d.id,
                    role='S')
        self.session.add(e)
        self.session.commit()

    def get_employees(self):
        return Employee.getall(self.session)

    def get_roles(self):
        roles = Employee.EMPLOYEE_ROLES
        result = [r[1] for r in roles]
        return result

    def get_managers(self):
        return Manager.getall(self.session)

    def get_commercials(self):
        return Commercial.getall(self.session)

    def get_supports(self):
        return Support.getall(self.session)

    def update_profil(self, e, data):
        data['password'] = self.ph.hash(data['password'])
        e.update_profil(self.session, data)
        self.session.commit

    def get_rolecode(self, rolename):
        roles = Employee.EMPLOYEE_ROLES
        for r in roles:
            if rolename in r:
                return r[0]
        return None

    def create_employee(self, data):
        data['password'] = self.ph.hash(data['password'])
        role = self.get_rolecode(data['role'])
        match role:
            case 'M': d = Department.find_by_name(
                self.session, 'management department')
            case 'C': d = Department.find_by_name(
                self.session, 'commercial department')
            case 'S': d = Department.find_by_name(
                self.session, 'support department')

        e = Employee(
            username=data['username'],
            password=data['password'],
            email=data['email'],
            department_id=d.id,
            role=role)
        try:
            self.session.add(e)
            self.session.commit()
            DataView.display_data_update()
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()

    def check_support_update_or_delete(
            self, support_name, manager_name) -> bool:
        e_support = Support.find_by_username(self.session, support_name)
        for event in e_support.events:
            event.support_id = None
            self.session.add(event)
            self.create_task(
                manager_name,
                EventView.workflow_ask_affect(event.title))
        return True

    def check_commercial_update_or_delete(self, commercial_name) -> bool:
        e_commercial = Commercial.find_by_username(
            self.session, commercial_name)
        for c in e_commercial.clients:
            if len(c.actif_contracts) > 0:
                DataView.display_commercial_with_contracts()
                return False
        return True

    def check_manager_update_or_delete(self) -> bool:
        e = Manager.getall(self.session)
        print(e)
        if len(e) == 1:
            DataView.display_need_one_manager()
            return False
        return True

    def check_role(self, employee, manager) -> bool:
        match employee.role.code:
            case 'S':
                return self.check_support_update_or_delete(
                    employee.username, manager.username)
            case 'C':
                return self.check_commercial_update_or_delete(
                    employee.username)
            case 'M':
                return self.check_manager_update_or_delete()

    def update_employee(self, name, role=None, password=None, manager=None):
        e = Employee.find_by_username(self.session, name)
        if role:
            if self.check_role(e, manager):
                e.role = self.get_rolecode(role)

        if password:
            e.password = self.ph.hash(password)

        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()

    def inactivate(self, name, manager):
        e = Employee.find_by_username(self.session, name)
        if self.check_role(e, manager):
            e.email = ''
            e.state = 'I'
            e.username = '<<' + e.username + '>>'
            self.session.add(e)
            self.session.commit()
            DataView.display_data_update()

    def get_tasks(self, e):
        return Task.find_active_tasks(self.session, e)

    def terminate_task(self, task_id):
        Task.terminate(self.session, task_id)
        self.session.commit()

    def create_task(self, employee_name, text):
        e = Employee.find_by_username(self.session, employee_name)
        t = Task(
            description=text,
            employee_id=e.id)
        self.session.add(t)
        self.session.commit()
        DataView.display_data_update()
