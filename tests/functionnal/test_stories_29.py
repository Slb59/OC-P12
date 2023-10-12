import epicevent
from ..mock_functions import MockFunction
from epicevents.views.client_views import ClientView
from epicevents.employee.employee_views import EmployeeView
from epicevents.views.auth_views import AuthView


def test_story_29(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_yuka)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ClientView,
        'prompt_data_client', MockFunction.mock_data_client)

    result = runner.invoke(epicevent.main, ['client', 'create'])
    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['client', 'list'])
    assert "NewClient" in result.output

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])
    result = runner.invoke(epicevent.main, ['employee', 'tasks'])
    assert "Creer le contrat du client NewClient" in result.output
