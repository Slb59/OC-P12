import pytest
import logging

from pytest import MonkeyPatch
from epicevents.controllers.epicmanager import EpicManager
from epicevents.employee.manager_employee import EpicManagerEmployee
from epicevents.controllers.session import create_session
from epicevents.views.auth_views import AuthView
from epicevents.views.console import error_console


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
    controle_employee = EpicManagerEmployee(app.user, app.epic)
    e = app.epic.check_connection('Osynia', 'osyA!111')
    create_session(e, app.env.TOKEN_DELTA, app.env.SECRET_KEY)
    controle_employee.list_of_employees()
    str_output = capsys.readouterr().out
    assert 'Osynia' in str_output


def test_login_fail():

    def new_prompt_login(*args, **kwargs):
        return ('Inconnu', 'incA?222')

    expected = "ERROR : Utilisateur ou mot de passe inconnu"
    with MonkeyPatch.context() as mp:
        mp.setattr(AuthView, 'prompt_manager', new_prompt_login)
        app = EpicManager()
        with error_console.capture() as capture:
            app.login()
        str_output = capture.get()
        assert expected in str_output
