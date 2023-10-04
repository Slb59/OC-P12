from pytest import MonkeyPatch
from sqlalchemy_utils import drop_database
from epicevents.controllers.database import EpicDatabase
from epicevents.views.auth_views import AuthView
from epicevents.models.entities import (
    Manager, Department, Commercial, Client)


def init_test_get_clients(epictest2):
    # given
    db = epictest2
    d = Department.find_by_name(db.session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    e2 = Commercial(username='Esumi', department_id=d.id, role='C')
    db.session.add_all([e1, e2])
    e1 = Commercial.find_by_username(db.session, 'Yuka')
    c1 = Client(full_name='c1', commercial_id=e1.id)
    e2 = Commercial.find_by_username(db.session, 'Esumi')
    c2 = Client(full_name='c2', commercial_id=e2.id)
    db.session.add_all([c1, c2])
    return db


def test_init_database(epictest2):
    db = epictest2
    assert str(db) == 'epictest2 database'


def test_database_creation():
    def new_prompt_manager(*args, **kwargs):
        return ('Osynia', 'osyA!111')

    with MonkeyPatch.context() as mp:
        mp.setattr(AuthView, 'prompt_manager', new_prompt_manager)
        db = EpicDatabase(
            "epictest2", "localhost", "postgres", "postG!111", "5432")
        drop_database(db.url)
        db = EpicDatabase(
            "epictest2", "localhost", "postgres", "postG!111", "5432")
        assert str(db) == 'epictest2 database'


def test_check_connection(epictest2):
    db = epictest2
    db.dbemployees.add_employee('Misoka', 'Misoka', 'Manager')
    e_base = Manager.find_by_username(db.session, 'Misoka')
    e_result = db.check_connection('Misoka', 'Misoka')
    assert e_base == e_result
    db.session.delete(e_result)
    db.session.commit()


def test_check_connection_error(epictest2):
    db = epictest2
    db.dbemployees.add_employee('Misoka2', 'Misoka', 'Manager')
    e_result = db.check_connection('Misoka2', 'Misoka2')
    assert e_result is None
    e = Manager.find_by_username(db.session, 'Misoka2')
    db.session.delete(e)
    db.session.commit()


def test_check_employee(epictest2):
    # given
    db = epictest2
    d = Department.find_by_name(db.session, 'management department')
    e = Manager(username='Yuka', department_id=d.id, role='C')
    db.session.add(e)
    # when
    result = db.check_employee('Yuka')
    # then
    assert result == e
