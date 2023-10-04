# import io
import pytest
import logging
# import mock
# import capsys
# from rich.console import Console
# from epicevents.views.console import console
from epicevents.controllers.epicmanager import EpicManager
from epicevents.controllers.session import create_session

log = logging.getLogger()


def test_init_epicmanager():
    app = EpicManager()
    assert str(app) == "CRM EPIC EVENTS"


def test_check_logout():
    # given
    app = EpicManager()
    # when
    app.check_logout()
    # then
    with pytest.raises(Exception) as e_info:
        open('session.json', 'r')
    assert e_info.type == FileNotFoundError


def test_list_of_employees(capsys):
    app = EpicManager()
    e = app.epic.check_connection('Osynia', 'osyA!111')
    create_session(e, app.env.TOKEN_DELTA, app.env.SECRET_KEY)
    app.list_of_employees()
    str_output = capsys.readouterr().out
    assert 'Osynia' in str_output


def test_create_new_employee(mocklogin, capsys):
    app = EpicManager()
    e = app.epic.check_connection('Osynia', 'osyA!111')
    create_session(e, app.env.TOKEN_DELTA, app.env.SECRET_KEY)
    # with mock.patch.object(__builtins__, 'input', lambda: 'some_input'):
    #     app.create_new_employee()
    assert False
