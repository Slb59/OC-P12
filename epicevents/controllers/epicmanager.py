from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
    )
from sqlalchemy import func
from .config import Config
from .database import EpicDatabase
from epicevents.models.entities import Client, Employee, Department


class EpicManager:

    def __init__(self) -> None:
        # load .env file
        db = Config()
        print(db)

        # create database
        self.epic = EpicDatabase(**db.db_config)

        # init data
        # login

    def __str__(self) -> str:
        return "CRM EPIC EVENTS"

    def run(self) -> None:

        # show menu
        running = True

        while running:

            Session = scoped_session(sessionmaker(bind=self.epic.engine))
            q = Session.query(Department)
            for _d in q.all():
                print(f'{_d.name}')
            client1 = Client(full_name='client 1')
            client2 = Client(full_name='client 2')
            employee = Employee(username='Yuka', department_id=3)
            client1.commercial = employee
            client2.commercial = employee
            Session.add(employee)
            Session.add(client1)
            Session.add(client2)
            q = Session.query(Client)
            for _c in q.all():
                print(f'{_c.full_name}')
            client1.full_name = 'client1b'
            Session.add(client1)
            q = Session.query(Employee, func.count(Client.id))\
                .join(Client)\
                .group_by(Employee.id)
            for _e, _c in q.all():
                print('employee: {}, nb_client: {}'.format(_e.username, _c))
            Session.commit()
            Session.remove()

            running = False
