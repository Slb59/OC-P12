import epicevent

from ..mock_functions import MockFunction
from epicevents.employee.employee_views import EmployeeView
from epicevents.client.client_views import ClientView
from epicevents.contract.contract_views import ContractView
from epicevents.views.prompt_views import PromptView
from epicevents.views.menu_views import MenuView
from epicevents.views.auth_views import AuthView


def test_story_17(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ClientView,
        'prompt_client', MockFunction.mock_client0)

    mp.setattr(
        ContractView,
        'prompt_data_contract', MockFunction.mock_prompt_data_contract)

    result = runner.invoke(epicevent.main, ['contract', 'create'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_yes)
    mp.setattr(
        PromptView, 'prompt_confirm_statut',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])
    assert not result.exception
    expected = "contrat0 │ Client n°0 │ 10000   │ 10000    "
    expected += "│ Créé"
    assert expected.replace(' ', '') in result.output.replace(' ', '')


def test_story_18_signacontract(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ClientView,
        'prompt_client', MockFunction.mock_client0)

    mp.setattr(
        ContractView,
        'prompt_data_contract', MockFunction.mock_prompt_data_contract)

    runner.invoke(epicevent.main, ['contract', 'create'])

    mp.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract0)

    mp.setattr(MenuView, 'menu_update_contract', MockFunction.mock_choice3)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_yes)
    mp.setattr(
        PromptView, 'prompt_confirm_statut',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])

    expected = "contrat0                    │ Client n°0 │ 10000   │ 10000    "
    expected += "│ Signé"
    assert expected in result.output
