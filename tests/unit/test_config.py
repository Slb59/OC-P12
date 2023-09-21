import pytest
from epicevents.controllers.config import (
    Config, NoSectionPostgresql, FileNotExists
)


def test_config_file_exists():
    config = Config()
    dict_to_result = ['database', 'host', 'user', 'password', 'port']
    assert list(config.db_config) == dict_to_result


def test_config_not_file():
    # given no file 'fichier.ini' 
    with pytest.raises(FileNotExists) as e_info:
        # when
        Config('fichier.ini')
        # then except FileEnvNotExists
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


