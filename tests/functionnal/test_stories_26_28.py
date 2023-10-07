import epicevent


def test_story_26(runner, epicstories):

    result = runner.invoke(epicevent.main, ['client', 'create'])

    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output

    result = runner.invoke(epicevent.main, ['client', 'update'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output

    result = runner.invoke(epicevent.main, ['event', 'create'])

    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output


def test_story_27(runner, epicstories_yuka):

    result = runner.invoke(epicevent.main, ['employee', 'create'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['employee', 'inactivate'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['employee', 'update-role'])
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


def test_story_28(runner, epicstories_aritomo):

    result = runner.invoke(epicevent.main, ['employee', 'create'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle manager requis." in result.output

    result = runner.invoke(epicevent.main, ['client', 'update'])
    assert not result.exception
    assert "ERROR : Accès refusé, rôle commercial requis." in result.output
