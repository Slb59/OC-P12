import epicevent

from epicevents.controllers.epicmanager import EpicManager
from epicevents.views.auth_views import AuthView
from ..mock_functions import MockFunction


def test_story_1(epicstories):

    (mp, runner) = epicstories
    expected = "La base epicStories est opérationnelle"

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)

    result = runner.invoke(epicevent.main, ['login'])

    assert not result.exception
    assert expected in result.output
    assert "ERROR" not in result.output


def test_story_2_and_3(epicstories):
    (mp, runner) = epicstories

    def new_prompt_login(*args, **kwargs):
        return ("Inconnu", "_")

    mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
    mp.setattr(AuthView, 'prompt_login', new_prompt_login)

    result = runner.invoke(epicevent.main, ['login'])

    assert not result.exception
    assert "ERROR" in result.output


def test_story_4(epicstories):
    (mp, runner) = epicstories
    expected = "Vous êtes déconnecté"

    mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
    mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)

    runner.invoke(epicevent.main, ['login'])
    result = runner.invoke(epicevent.main, ['logout'])
    assert not result.exception
    assert expected in result.output


def test_story_5(epicstories):
    (mp, runner) = epicstories

    mp.setattr(EpicManager, 'get_config', MockFunction.mock_base)
    mp.setattr(AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])
    result = runner.invoke(epicevent.main, ['employee', 'mydata'])
    runner.invoke(epicevent.main, ['logout'])

    assert not result.exception
    assert "Osynia" in result.output
