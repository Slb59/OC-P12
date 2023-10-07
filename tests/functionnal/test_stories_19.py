import epicevent

from ..mock_functions import MockFunction
from epicevents.views.event_views import EventView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.contract_views import ContractView
from epicevents.views.auth_views import AuthView


def test_story_19(runner, epicstories):
    epicstories.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    epicstories.setattr(
        EmployeeView,
        'prompt_select_support', MockFunction.mock_aritomo)

    epicstories.setattr(
        ClientView,
        'prompt_client', MockFunction.mock_client0)

    epicstories.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    epicstories.setattr(
        EventView,
        'prompt_select_event', MockFunction.mock_event_contract1)

    result = runner.invoke(epicevent.main, ['event', 'update'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
