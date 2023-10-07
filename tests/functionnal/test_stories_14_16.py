import epicevent

from ..mock_functions import MockFunction
from epicevents.views.employee_views import EmployeeView


def test_story_14(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_employee_support)

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])
    result3 = runner.invoke(epicevent.main, ['employee', 'tasks'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "<<Aritomo>> │       │ Support    │ Inactif" in result2.output
    assert "Affecter un support pour l'évènement Aritomo" in result3.output


def test_story_15_with_clients(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_yuka)

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Ce commercial gère des contracts actifs" in result.output
    assert "Yuka        │       │ Commercial" in result2.output


def test_story_15_without_clients(runner, epicstories):

    epicstories.setattr(EmployeeView,
                        'prompt_employee', MockFunction.mock_morihei)

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "<<Morihei>> │       │ Commercial │ Inactif" in result2.output


def test_story_16_fail(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_osynia)

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "La base doit contenir au moins un manager" in result.output
    assert "Osynia      │       │ Manager" in result2.output


def test_story_16(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_role', MockFunction.mock_role_manager)

    epicstories.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_morihei)
    result = runner.invoke(epicevent.main, ['employee', 'update-role'])

    epicstories.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_morihei)

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "<<Morihei>> │       │ Manager    │ Inactif" in result2.output
