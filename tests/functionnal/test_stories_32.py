import epicevent
from ..mock_functions import MockFunction
from epicevents.views.business_views.event_views import EventView
from epicevents.views.business_views.contract_views import ContractView
from epicevents.views.business_views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.auth_views import AuthView


def test_story_32(epicstories):
    (mp, runner) = epicstories

    def mock_select_event(*args, **kwargs):
        return 'contrat1|Aritomo event'

    def mock_prompt_rapport(*args, **kwargs):
        return 'Evenement termine avec success'

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_aritomo)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EventView,
        'prompt_select_event', mock_select_event)

    mp.setattr(
        EventView,
        'prompt_rapport', mock_prompt_rapport)

    mp.setattr(
        ContractView, 'prompt_confirm_close_contract',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['event', 'close'])
    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
        EmployeeView, 'prompt_confirm_commercial',
        MockFunction.mock_prompt_confirm_yes)
    mp.setattr(
        EmployeeView, 'prompt_commercial', MockFunction.mock_yuka)
    mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ContractView,
            'prompt_confirm_contract',
            MockFunction.mock_prompt_confirm_yes)
    mp.setattr(
            ContractView, 'prompt_select_contract',
            MockFunction.mock_contract1)
    mp.setattr(
            EmployeeView,
            'prompt_confirm_support',
            MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['event', 'list'])
    assert not result.exception
    expected = "Aritomo event  │ somewhere │ 10               │ "
    expected += "du 07/10/2023-15h00 │ Terminé"
    assert expected.replace(" ", "") in result.output.replace(" ", "")
