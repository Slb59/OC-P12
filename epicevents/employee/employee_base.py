from argon2 import PasswordHasher
from sqlalchemy.exc import IntegrityError
from epicevents.views.data_views import DataView
from epicevents.event.event_views import EventView
from epicevents.models.entities import (
    Department, Manager, Commercial, Support,
    Employee, Task
)


class EmployeeBase:

    """ Manage crud operations on Employee base """

    def __init__(self, session) -> None:
        self.ph = PasswordHasher()
        self.session = session

    def add_employee(self, username, password, role) -> None:
        """ add an employee in database

        Args:
            username (str): a username
            password (str): a clear password
            role (str): a role name
        """

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

    def get_employees(self) -> list:
        """ give all employees in database

        Returns:
            list: list of employee instance
        """
        return Employee.getall(self.session)

    def get_roles(self) -> list:
        """ give the list of role name """
        roles = Employee.EMPLOYEE_ROLES
        result = [r[1] for r in roles]
        return result

    def get_managers(self) -> list:
        """ give all the managers of the database

        Returns:
            list: list of instance of Manager
        """
        return Manager.getall(self.session)

    def get_commercials(self) -> list:
        """ give all the commercials of the database

        Returns:
            list: list of instance of Commercial
        """
        return Commercial.getall(self.session)

    def get_supports(self):
        """ give all the supports of the database

        Returns:
            list: list of instance of Support
        """
        return Support.getall(self.session)

    def update_profil(self, e, data) -> None:
        """ update the data of an employee

        Args:
            e (Employee): an instance of Employee
            data (dict): example
            {'username': username, 'password': password, 'email': email}
        """
        e.username = data['username']\
            if data['username'] else e.username
        e.password = self.ph.hash(data['password'])\
            if data['password'] else e.password
        e.email = data['email']\
            if data['email'] else e.email
        self.session.add(e)
        self.session.commit

    def get_rolecode(self, rolename) -> str:
        """ give the role code for a role name

        Args:
            rolename (str): role name

        Returns:
            str: role code
        """
        roles = Employee.EMPLOYEE_ROLES
        for r in roles:
            if rolename in r:
                return r[0]
        return None

    def create_employee(self, data) -> None:
        """ create a new employee in database

        Args:
            data (dict): example
            {'username': username, 'password': password,
            'email': email, 'role': 'Manager'}
        """
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
        """ set alls events of a support to None
        and generate workflow for the manager

        Args:
            support_name (str): support username
            manager_name (str): manager username

        Returns:
            bool: always True
        """
        e_support = Support.find_by_username(self.session, support_name)
        for event in e_support.events:
            event.support_id = None
            self.session.add(event)
            self.create_task(
                manager_name,
                EventView.workflow_ask_affect(event.title))
        return True

    def check_commercial_update_or_delete(self, commercial_name) -> bool:
        """ check if commercial has a client with active contract

        Args:
            commercial_name (str): commercial username

        Returns:
            bool: False if commercial has active contract
            else True
        """
        e_commercial = Commercial.find_by_username(
            self.session, commercial_name)
        for c in e_commercial.clients:
            if len(c.actif_contracts) > 0:
                DataView.display_commercial_with_contracts()
                return False
        return True

    def check_manager_update_or_delete(self) -> bool:
        """ check if there is at least one manager left

        Returns:
            bool: True if there is more than one manager
            else False
        """
        e = Manager.getall(self.session)
        if len(e) == 1:
            DataView.display_need_one_manager()
            return False
        return True

    def check_role(self, employee, manager) -> bool:
        """ check if employee can be updated or deleted

        Args:
            employee (Employee): a Employee instance
            manager (Manager): a Manager instance

        Returns:
            bool: True or False
        """
        match employee.role.code:
            case 'S':
                return self.check_support_update_or_delete(
                    employee.username, manager.username)
            case 'C':
                return self.check_commercial_update_or_delete(
                    employee.username)
            case 'M':
                return self.check_manager_update_or_delete()

    def update_employee(
            self, name, role=None, password=None, manager=None) -> None:
        """ update data of an employee

        Args:
            name (str): Employee username
            role (str, optional): Role name. Defaults to None.
            password (str, optional): a clear password. Defaults to None.
            manager (Manager, optional): an instance of manager.
            Defaults to None.
        """
        e = Employee.find_by_username(self.session, name)
        if role:
            if self.check_role(e, manager):
                e.role = self.get_rolecode(role)

        if password:
            e.password = self.ph.hash(password)

        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()

    def inactivate(self, name, manager) -> None:
        """ set state at I=Inactivate if it's possible

        Args:
            name (str): employee username
            manager (Manager): instance of Manager
        """
        e = Employee.find_by_username(self.session, name)
        if self.check_role(e, manager):
            e.email = ''
            e.state = 'I'
            e.username = '<<' + e.username + '>>'
            self.session.add(e)
            self.session.commit()
            DataView.display_data_update()

    def get_tasks(self, e) -> list:
        """ give the list of active tasks

        Args:
            e (Employee): instance of employee

        Returns:
            list: list of instance of tasks
        """
        return Task.find_active_tasks(self.session, e)

    def terminate_task(self, task_id) -> None:
        """ change state of task to terminate

        Args:
            task_id (str): a task id
        """
        Task.terminate(self.session, task_id)
        self.session.commit()

    def create_task(self, employee_name, text) -> None:
        """ create a new task for the employee

        Args:
            employee_name (str): Employee username
            text (str): the description of what todo
        """
        e = Employee.find_by_username(self.session, employee_name)
        t = Task(
            description=text,
            employee_id=e.id)
        self.session.add(t)
        self.session.commit()
        DataView.display_data_update()
