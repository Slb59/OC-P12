from argon2 import PasswordHasher
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
        # hashed_password = password

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

        self.session.add(e)

    def update_employee(self, name, role):
        e = Employee.find_by_username(self.session, name)
        e.role = self.get_rolecode(role)
        self.session.add(e)
        self.session.commit()

    def inactivate(self, name):
        e = Employee.find_by_username(self.session, name)
        check = True
        if e.role == 'C':
            e = Commercial.find_by_username(self.session, name)
            for c in e.clients:
                if len(c.actif_contracts) > 0:
                    check = False
        if e.role == 'S':
            e = Support.find_by_username(self.session, name)
            for event in e.events:
                event.support_id = None
                self.session.add(event)
                description = "Ajouter un support à l'évènement "
                description += event.title + " du contrat "
                description += event.contract.ref
                manager = Manager.getone(self.session)
                t = Task(description=description, employee_id=manager.id)
                self.session.add(t)
        if check:
            e.email = ''
            e.state = 'I'
            e.username = '<<' + e.username + '>>'
            self.session.add(e)
            self.session.commit()
