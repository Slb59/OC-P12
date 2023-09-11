# import psycopg2

# conn = psycopg2.connect(database="db_name",
#                         host="db_host",
#                         user="db_user",
#                         password="db_pass",
#                         port="db_port")

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy_utils import database_exists, create_database, drop_database
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
    )
from epicevents.models.entities import Base, Department


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
        drop_database(url)

        if not database_exists(url):
            print('no database --> creating one')
            create_database(url)
            # init database structure
            engine = create_engine(url)
            Base.metadata.create_all(engine)
            Session = scoped_session(sessionmaker(bind=engine))
            management_dpt = Department(name='management department')
            support_dpt = Department(name='support department')
            commercial_dpt = Department(name='commercial department')
            Session.add_all([management_dpt, support_dpt, commercial_dpt])
            Session.commit()
            Session.remove()

        self.engine = create_engine(url)
