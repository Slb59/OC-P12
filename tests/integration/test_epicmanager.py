# import io
import pytest
import logging
# import mock
# import capsys
# from rich.console import Console
# from epicevents.views.console import console
from epicevents.controllers.epicmanager import EpicManager

log = logging.getLogger()


def test_init_epicmanager(mockparser):
    app = EpicManager(mockparser)
    assert str(app) == "CRM EPIC EVENTS"


def test_check_logout(mockparser):
    # given
    mockparser.logout = True
    app = EpicManager(mockparser)
    # when
    app.check_logout()
    # then
    with pytest.raises(Exception) as e_info:
        open('session.json', 'r')
    assert e_info.type == FileNotFoundError


def test_list_of_employees(mockparser, mocklogin, capsys):
    mockparser.login = mocklogin
    app = EpicManager(mockparser)
    app.check_login()
    app.list_of_employees()
    str_output = capsys.readouterr().out
    assert 'Osynia' in str_output


def test_create_new_employee(mockparser, mocklogin, capsys):
    mockparser.login = mocklogin
    app = EpicManager(mockparser)
    app.check_login()
    # with mock.patch.object(__builtins__, 'input', lambda: 'some_input'):
    #     app.create_new_employee()
    assert False
