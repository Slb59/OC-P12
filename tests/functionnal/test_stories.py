import epicevent
from pytest import MonkeyPatch

from epicevents.views.auth_views import AuthView
from epicevents.views.employee_views import EmployeeView


def mock_prompt_login():
    return ("Osynia", "osyA!111")


def mock_prompt_confirm_no():
    return False


def mock_prompt_confirm_yes():
    return True


def mock_prompt_commercial(*args, **kwargs):
    return 'Yuka'


def test_story_1(runner):

    expected = "La base epicT est opérationnelle"

    with MonkeyPatch.context() as mp:
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)

        result = runner.invoke(epicevent.main, ['login'])

        assert not result.exception
        assert expected in result.output
        assert "ERROR" not in result.output


def test_story_2_and_3(runner):

    def new_prompt_login(*args, **kwargs):
        return ("Inconnu", "_")

    with MonkeyPatch.context() as mp:
        mp.setattr(AuthView, 'prompt_login', new_prompt_login)

        result = runner.invoke(epicevent.main, ['login'])

        assert not result.exception
        assert "ERROR" in result.output


def test_story_4(runner):
    expected = "Vous êtes déconnecté"

    with MonkeyPatch.context() as mp:
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['logout'])
        assert not result.exception
        assert expected in result.output


def test_story_5_no_selection(runner):

    with MonkeyPatch.context() as mp:
        mp.setattr(AuthView, 'prompt_login', mock_prompt_login)
        mp.setattr(
            EmployeeView, 'prompt_confirm_commercial', mock_prompt_confirm_no)

        runner.invoke(epicevent.main, ['login'])
        result = runner.invoke(epicevent.main, ['client', 'list'])
        runner.invoke(epicevent.main, ['logout'])

        assert not result.exception
        assert "Liste des clients" in result.output


def test_story_5_with_commercial(runner):

    with MonkeyPatch.context() as mp:
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


def test_story_6(capsys):
    # app = EpicManager('None')
    # app.run()
    assert False
