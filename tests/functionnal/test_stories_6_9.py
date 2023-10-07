import epicevent
from pytest import MonkeyPatch

from ..mock_functions import MockFunction
from epicevents.controllers.epicmanager import EpicManager
from epicevents.views.auth_views import AuthView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.prompt_views import PromptView
from epicevents.views.contract_views import ContractView


def test_story_6_no_selection(runner):

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
        mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
        mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['client', 'list'])
        runner.invoke(epicevent.main, ['logout'])

        assert not result.exception
        assert "Liste des clients" in result.output


def test_story_6_with_commercial(runner):

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
        mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
        mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_yes)
        mp.setattr(
            EmployeeView,
            'prompt_commercial',
            MockFunction.mock_prompt_commercial)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['client', 'list'])
        runner.invoke(epicevent.main, ['logout'])

        assert not result.exception
        assert "Yuka" in result.output
        assert "Esumi" not in result.output


def test_story_7_noselection(runner):
    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
        mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
        mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
        mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
        mp.setattr(PromptView,
                   'prompt_confirm_statut',
                   MockFunction.mock_prompt_confirm_no)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['contract', 'list'])
        runner.invoke(epicevent.main, ['logout'])

    assert not result.exception
    assert "Liste des contracts" in result.output


def test_story_8_noselection(runner):
    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
        mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
        mp.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)
        mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
        mp.setattr(
            ContractView,
            'prompt_confirm_contract',
            MockFunction.mock_prompt_confirm_no)
        mp.setattr(
            EmployeeView,
            'prompt_confirm_support',
            MockFunction.mock_prompt_confirm_no)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['event', 'list'])
        runner.invoke(epicevent.main, ['logout'])

    assert not result.exception
    assert "Liste des évènements" in result.output


def test_story_9(runner):
    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
        mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['employee', 'tasks'])
        runner.invoke(epicevent.main, ['logout'])
    assert not result.exception
    assert "Mes tâches à réaliser" in result.output
