import epicevent
from pytest import MonkeyPatch

from epicevents.controllers.config import Config
from epicevents.controllers.epicmanager import EpicManager
from epicevents.views.auth_views import AuthView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView
from epicevents.views.prompt_views import PromptView


def mock_base(*args, **kwargs):
    return Config('tests/functionnal/database_userstories.ini')


def mock_prompt_login():
    return ("Osynia", "osyA!111")


def mock_prompt_confirm_no():
    return False


def mock_prompt_confirm_yes():
    return True


def mock_prompt_commercial(*args, **kwargs):
    return 'Yuka'


def test_story_1(runner):

    expected = "La base epicStories est opérationnelle"

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)

        result = runner.invoke(epicevent.main, ['login'])

        assert not result.exception
        assert expected in result.output
        assert "ERROR" not in result.output


def test_story_2_and_3(runner):

    def new_prompt_login(*args, **kwargs):
        return ("Inconnu", "_")

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', new_prompt_login)

        result = runner.invoke(epicevent.main, ['login'])

        assert not result.exception
        assert "ERROR" in result.output


def test_story_4(runner):
    expected = "Vous êtes déconnecté"

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['logout'])
        assert not result.exception
        assert expected in result.output


def test_story_5(runner):

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)
        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['employee', 'mydata'])
        runner.invoke(epicevent.main, ['logout'])

        assert not result.exception
        assert "Osynia" in result.output


def test_story_6_no_selection(runner):

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)
        mp.setattr(
            EmployeeView, 'prompt_confirm_commercial', mock_prompt_confirm_no)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['client', 'list'])
        runner.invoke(epicevent.main, ['logout'])

        assert not result.exception
        assert "Liste des clients" in result.output


def test_story_6_with_commercial(runner):

    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)
        mp.setattr(
            EmployeeView, 'prompt_confirm_commercial', mock_prompt_confirm_yes)
        mp.setattr(
            EmployeeView, 'prompt_commercial', mock_prompt_commercial)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['client', 'list'])
        runner.invoke(epicevent.main, ['logout'])

        assert not result.exception
        assert "Yuka" in result.output
        assert "Esumi" not in result.output


def test_story_7_noselection(runner):
    with MonkeyPatch.context() as mp:
        mp.setattr(EpicManager, 'get_config', mock_base)
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)
        mp.setattr(
            EmployeeView, 'prompt_confirm_commercial', mock_prompt_confirm_no)
        mp.setattr(ClientView, 'prompt_confirm_client', mock_prompt_confirm_no)
        mp.setattr(PromptView, 'prompt_confirm_statut', mock_prompt_confirm_no)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['contract', 'list'])
        runner.invoke(epicevent.main, ['logout'])

    assert not result.exception
    assert "Liste des contracts" in result.output
