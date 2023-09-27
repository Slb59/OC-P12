import pytest
import argparse
from datetime import datetime
from freezegun import freeze_time
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, drop_database
from epicevents.models.entities import Base, Task

TEST_DB_NAME = "epictest"


def pytest_addoption(parser):
    parser.addoption(
        '--dburl',
        action='store',
        default='postgresql://postgres:postgres@localhost:5432/epictest',
        help='postgresql://postgres:postgres@localhost:5432/epictest'
        )


@pytest.fixture()
def db_url(request):
    return request.config.getoption("--dburl")


@pytest.fixture(scope='session')
def db_engine(request):
    """yields a SQLAlchemy engine which is suppressed after the test session"""
    db_url = request.config.getoption("--dburl")
    create_database(db_url)
    engine_ = create_engine(db_url, echo=True)
    Base.metadata.create_all(engine_)
    yield engine_
    engine_.dispose()
    drop_database(db_url)


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    """returns a SQLAlchemy scoped session factory"""
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    yield session_
    session_.rollback()
    session_.close()


@pytest.fixture(scope='function')
def db_session_no_rollback(db_session_factory):
    """yields a SQLAlchemy connection which is rollbacked after the test"""
    session_ = db_session_factory()
    yield session_
    session_.close()


@contextmanager
def patch_time(time_to_freeze, tick=True):
    with freeze_time(time_to_freeze, tick=tick) as frozen_time:
        def set_timestamp(mapper, connection, target):
            now = datetime.now()
            if hasattr(target, 'started_time'):
                target.created = now
        event.listen(Task, 'before_insert', set_timestamp,
                     propagate=True)
        yield frozen_time
        event.remove(Task, 'before_insert', set_timestamp)


@pytest.fixture(scope='function')
def patch_current_time():
    return patch_time


@pytest.fixture(scope='function')
def mockparser():
    parser = argparse.ArgumentParser(
        prog="EpicEvent-Test",
        description="Gestionnaire d'évènements",
        epilog="------ CRM EpicEvent ------"
    )
    return parser


@pytest.fixture(scope='function')
def mocklogin():
    return 'Osynia/osyA!111'
