from sqlalchemy_utils import drop_database
from epicevents.controllers.database import EpicDatabase
from epicevents.models.entities import Manager


def test_init_database():
    db = EpicDatabase('epictest', "localhost", "postgres", "postgres", "5432")
    assert str(db) == 'epictest database'
    drop_database(db.url)


def test_check_connection():
    db = EpicDatabase('epictest', "localhost", "postgres", "postgres", "5432")
    db.add_employee('Misoka', 'Misoka', 'Manager')
    e_base = Manager.find_by_username(session=db.session, username='Misoka')
    print(e_base.username)
    e_result = db.check_connection('Misoka', 'Misoka')
    assert e_base == e_result
    drop_database(db.url)
