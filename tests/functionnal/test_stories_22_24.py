import epicevent

from ..mock_functions import MockFunction
from epicevents.contract.contract_views import ContractView
from epicevents.views.menu_views import MenuView
from epicevents.employee.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.prompt_views import PromptView
from epicevents.views.auth_views import AuthView


def test_story_22(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    mp.setattr(
        MenuView,
        'menu_update_contract', MockFunction.mock_choice1)

    mp.setattr(
        ContractView,
        'prompt_data_paiement', MockFunction.mock_data_paiement_1000)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
        PromptView,
        'prompt_confirm_statut',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])

    assert not result.exception
    expected = "contrat1  │ Client n°0  "
    expected += "│ 3000    │ 2000     │ Signé"
    assert expected.replace(' ', '') in result.output.replace(' ', '')


def test_story_23(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    mp.setattr(
        MenuView,
        'menu_update_contract', MockFunction.mock_choice1)

    mp.setattr(
        ContractView,
        'prompt_data_paiement', MockFunction.mock_data_paiement_3000)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
        PromptView,
        'prompt_confirm_statut',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])

    assert not result.exception
    expected = "contrat1                    │ Client n°0  "
    expected += "│ 3000    │ 0        │ Soldé"
    assert expected.replace(' ', '') in result.output.replace(' ', '')


def test_story_24(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    mp.setattr(
        MenuView,
        'menu_update_contract', MockFunction.mock_choice1)

    mp.setattr(
        ContractView,
        'prompt_data_paiement', MockFunction.mock_data_paiement_4000)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert not result.exception
    assert "Ce montant est supérieur au restant dû" in result.output
