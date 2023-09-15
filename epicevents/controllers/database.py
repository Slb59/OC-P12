from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
    )
from sqlalchemy.exc import ProgrammingError
from epicevents.models.entities import Base, Department, Manager


class EpicDatabase:

    def __init__(self, database, host, user, password, port) -> None:

        url = URL.create(
            drivername="postgresql",
            database=database,
            host=host,
            username=user,
            password=password,
            port=int(port)
        )

        print(url)

        try:
            drop_database(url)
        except ProgrammingError:
            ...

        # if not database_exists(url):
        if True:
            print('no database --> creating one')
            create_database(url)
            # init database structure
            engine = create_engine(url)
            Base.metadata.create_all(engine)
            self.session = scoped_session(sessionmaker(bind=engine))
            self.first_initdb()
            self.session.remove()

        self.engine = create_engine(url)

        self.session = scoped_session(sessionmaker(bind=self.engine))

    def first_initdb(self):
        # add departments
        management_dpt = Department(name='management department')
        support_dpt = Department(name='support department')
        commercial_dpt = Department(name='commercial department')
        self.session.add_all([management_dpt, support_dpt, commercial_dpt])
        self.session.commit()
        # add a manager
        d = Department.find_by_name(self.session, 'management department')
        e = Manager(
            username='Osynia',
            password='osyA!111',
            department_id=d.id,
            role='M')
        self.session.add(e)
        self.session.commit()
