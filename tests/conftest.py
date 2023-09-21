import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_utils import create_database, drop_database
from epicevents.models.entities import Base

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
    print(db_url)
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
