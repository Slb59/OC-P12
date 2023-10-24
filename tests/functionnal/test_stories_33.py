import epicevent
from ..mock_functions import MockFunction
from epicevents.employee.employee_views import EmployeeView
from epicevents.client.client_views import ClientView
from epicevents.views.auth_views import AuthView


def test_story_33(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_yuka)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView, 'prompt_manager', MockFunction.mock_osynia)
    mp.setattr(
        ClientView, 'prompt_client', MockFunction.mock_clientyuka)

    result = runner.invoke(epicevent.main, ['employee', 'task-contract'])
    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])
    result = runner.invoke(epicevent.main, ['employee', 'tasks'])
    expected = " Creer le contrat du client YukaCli"
    assert expected in result.output
