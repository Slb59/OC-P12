from sqlalchemy_utils import drop_database
from epicevents.controllers.database import EpicDatabase
from epicevents.models.entities import Manager


def test_init_database():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    drop_database(db.url)
    assert str(db) == 'epictest2 database'


def test_check_connection():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.add_employee('Misoka', 'Misoka', 'Manager')
    e_base = Manager.find_by_username(session=db.session, username='Misoka')
    e_result = db.check_connection('Misoka', 'Misoka')
    drop_database(db.url)
    assert e_base == e_result


def test_check_connection_error():
    db = EpicDatabase('epictest2', "localhost", "postgres", "postgres", "5432")
    db.add_employee('Misoka', 'Misoka', 'Manager')
    e_result = db.check_connection('Misoka', 'Misoka2')
    drop_database(db.url)
    assert e_result is None
