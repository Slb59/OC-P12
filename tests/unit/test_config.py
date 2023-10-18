import pytest
from epicevents.controllers.config import (
    Config, NoSectionPostgresql, FileNotExists,
    Environ
)


def test_init_config():
    s = "{'database': 'epic', 'host': 'localhost', "
    s += "'user': 'postgres', 'password': 'postG!111', 'port': '5432'}"
    config = Config('tests/unit/database_test.ini')
    print(config)
    assert str(config) == s


def test_config_file_exists():
    config = Config('tests/unit/database_test.ini')
    dict_to_result = ['database', 'host', 'user', 'password', 'port']
    assert list(config.db_config) == dict_to_result


def test_config_not_file():
    # GIVEN no file 'fichier.ini'
    with pytest.raises(FileNotExists) as e_info:
        # WHEN
        Config('fichier.ini')
        # THEN except FileEnvNotExists
    msg = "the file fichier.ini doesn't exists"
    assert str(e_info.value) == msg


def test_config_not_exists():
    # given 'database_test_error.ini'
    with pytest.raises(NoSectionPostgresql) as e_info:
        # when
        Config('tests/unit/database_test_error.ini')
        # then except NoSectionPostgresql
    msg = "the file database.ini doesn't have postgresql section"
    assert str(e_info.value) == msg


def test_init_environ():
    env = Environ()
    assert env.DEFAULT_DATABASE == 'epicTestA'
    assert env.SECRET_KEY == 'm59r06yt*+d4h8zo@fx0%@y3jn*$^(!$)_m30k=9qov4jmx&'
    assert env.TOKEN_DELTA > 1
