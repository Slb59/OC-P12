import epicevent
from ..mock_functions import MockFunction
from epicevents.views.client_views import ClientView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.auth_views import AuthView


def test_story_29(runner, epicstories_yuka):

    epicstories_yuka.setattr(
        ClientView,
        'prompt_data_client', MockFunction.mock_data_client)

    result = runner.invoke(epicevent.main, ['client', 'create'])
    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    epicstories_yuka.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['client', 'list'])
    assert "NewClient" in result.output

    epicstories_yuka.setattr(AuthView, 'prompt_login',
                             MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])
    result = runner.invoke(epicevent.main, ['employee', 'tasks'])
    assert "Creer le contrat du client NewClient" in result.output
