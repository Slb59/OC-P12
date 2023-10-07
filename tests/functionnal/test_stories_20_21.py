import epicevent


def test_story_20(runner, epicstories):

    result = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Esumi       │       │ Commercial │ Actif" in result.output


def test_story_21(runner, epicstories):

    result = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Aritomo     │       │ Support    │ Actif" in result.output
