import pytest
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session
    )


def test_list_department(mocker, mock_session):
    """
    create session on epic database
    """
    url = URL.create(
        drivername="postgresql",
        database="epic",
        host="localhost",
        username="postgres",
        password="vplWta!0809p",
        port=int(5432)
    )
    engine = create_engine(url)
    self.session = scoped_session(sessionmaker(bind=engine))