import epicevent

from ..mock_functions import MockFunction
from epicevents.views.contract_views import ContractView
from epicevents.views.menu_views import MenuView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.prompt_views import PromptView


def test_story_22(runner, epicstories):

    epicstories.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    epicstories.setattr(
        MenuView,
        'menu_update_contract', MockFunction.mock_choice1)

    epicstories.setattr(
        ContractView,
        'prompt_data_paiement', MockFunction.mock_data_paiement_1000)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    epicstories.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    epicstories.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
    epicstories.setattr(
        PromptView,
        'prompt_confirm_statut',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])

    assert not result.exception
    expected = "contrat1                    │ Client n°0  "
    expected += "│ 3000    │ 2000     │ Signé"
    assert expected in result.output


def test_story_23(runner, epicstories):

    epicstories.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    epicstories.setattr(
        MenuView,
        'menu_update_contract', MockFunction.mock_choice1)

    epicstories.setattr(
        ContractView,
        'prompt_data_paiement', MockFunction.mock_data_paiement_3000)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    epicstories.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    epicstories.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
    epicstories.setattr(
        PromptView,
        'prompt_confirm_statut',
        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])

    assert not result.exception
    expected = "contrat1                    │ Client n°0  "
    expected += "│ 3000    │ 0        │ Soldé"
    assert expected in result.output
