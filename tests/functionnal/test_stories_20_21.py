import epicevent
from ..mock_functions import MockFunction
from epicevents.views.auth_views import AuthView


def test_story_20(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    result = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Esumi       │       │ Commercial │ Actif" in result.output


def test_story_21(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    result = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Aritomo     │       │ Support    │ Actif" in result.output
