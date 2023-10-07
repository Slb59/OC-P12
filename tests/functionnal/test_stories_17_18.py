import epicevent

from ..mock_functions import MockFunction
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.contract_views import ContractView
from epicevents.views.prompt_views import PromptView
from epicevents.views.menu_views import MenuView


def test_story_17(runner, epicstories):

    epicstories.setattr(
        ClientView,
        'prompt_client', MockFunction.mock_client0)

    epicstories.setattr(
        ContractView,
        'prompt_data_contract', MockFunction.mock_prompt_data_contract)

    result = runner.invoke(epicevent.main, ['contract', 'create'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    epicstories.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    epicstories.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_yes)
    epicstories.setattr(PromptView, 'prompt_confirm_statut',
                        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])
    assert not result.exception
    expected = "contrat0                    │ Client n°0 │ 10000   │ 10000    "
    expected += "│ Créé"
    assert expected in result.output


def test_story_18_signacontract(runner, epicstories):

    epicstories.setattr(
        ClientView,
        'prompt_client', MockFunction.mock_client0)

    epicstories.setattr(
        ContractView,
        'prompt_data_contract', MockFunction.mock_prompt_data_contract)

    runner.invoke(epicevent.main, ['contract', 'create'])

    epicstories.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract0)

    epicstories.setattr(MenuView,
                        'menu_update_contract', MockFunction.mock_choice3)

    result = runner.invoke(epicevent.main, ['contract', 'update'])

    assert "Vos modifications ont été enregistrées" in result.output

    epicstories.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
    epicstories.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_yes)
    epicstories.setattr(PromptView, 'prompt_confirm_statut',
                        MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['contract', 'list'])

    expected = "contrat0                    │ Client n°0 │ 10000   │ 10000    "
    expected += "│ Signé"
    assert expected in result.output
