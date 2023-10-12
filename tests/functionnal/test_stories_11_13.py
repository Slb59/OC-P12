import epicevent

from ..mock_functions import MockFunction
from epicevents.employee.employee_views import EmployeeView
from epicevents.views.auth_views import AuthView


def test_story_11(epicstories):
    (mp, runner) = epicstories

    mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView, 'prompt_role', MockFunction.mock_role_manager)
    mp.setattr(
        EmployeeView, 'prompt_employee', MockFunction.mock_aritomo)

    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])
    result3 = runner.invoke(epicevent.main, ['employee', 'tasks'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "Aritomo     │       │ Manager" in result2.output
    assert "Affecter un support pour l'évènement Aritomo" in result3.output


def test_story_12_with_clients(epicstories):

    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView, 'prompt_role', MockFunction.mock_role_manager)
    mp.setattr(
        EmployeeView, 'prompt_employee', MockFunction.mock_yuka)

    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Ce commercial gère des contracts actifs" in result.output
    expected = "Yuka││Commercial"
    assert expected in result2.output.replace(" ", "")


def test_story_12_without_clients(epicstories):
    (mp, runner) = epicstories

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView, 'prompt_role', MockFunction.mock_role_manager)
    mp.setattr(
        EmployeeView, 'prompt_employee', MockFunction.mock_morihei)

    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "Morihei     │       │ Manager" in result2.output


def test_story_13_fail(epicstories):

    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView,
        'prompt_role', MockFunction.mock_role_commercial)
    mp.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_osynia)

    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "La base doit contenir au moins un manager" in result.output
    assert "Osynia      │       │ Manager" in result2.output


def test_story_13(epicstories):

    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView,
        'prompt_role', MockFunction.mock_role_manager)
    mp.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_morihei)
    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])

    mp.setattr(
        EmployeeView,
        'prompt_role', MockFunction.mock_role_commercial)
    mp.setattr(EmployeeView, 'prompt_employee', MockFunction.mock_osynia)

    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "ERROR : Accès refusé, rôle manager requis." in result2.output
