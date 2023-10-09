import epicevent
from ..mock_functions import MockFunction
from epicevents.views.auth_views import AuthView


def test_story_26(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    result = runner.invoke(epicevent.main, ['client', 'create'])

    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output

    result = runner.invoke(epicevent.main, ['client', 'update'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output

    result = runner.invoke(epicevent.main, ['event', 'create'])

    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output


def test_story_27(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_yuka)
    runner.invoke(epicevent.main, ['login'])

    result = runner.invoke(epicevent.main, ['employee', 'create'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['employee', 'updaterole'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['contract', 'create'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['contract', 'update'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['event', 'update'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output


def test_story_28(epicstories):
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_aritomo)
    runner.invoke(epicevent.main, ['login'])

    result = runner.invoke(epicevent.main, ['employee', 'create'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['client', 'update'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output
