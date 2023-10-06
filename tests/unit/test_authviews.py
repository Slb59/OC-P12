from epicevents.views.auth_views import AuthView
from ..utils import (KeyInputs, ask_with_patched_input)


def test_prompt_login():
    values = ('Identifiant', 'monPass!111')
    text = values[0] + KeyInputs.ENTER + values[1] + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(AuthView.prompt_login, text)
    assert result == values


def test_prompt_baseinit():
    values = ('epic', 'postgres', 'postGres!111', '1235')
    text = values[0] + KeyInputs.ENTER\
        + values[1] + KeyInputs.ENTER\
        + values[2] + KeyInputs.ENTER\
        + values[3] + KeyInputs.ENTER\
        + "\r"
    result = ask_with_patched_input(AuthView.prompt_baseinit, text)
    assert result == values


def test_prompt_manager():
    values = ('osynia', 'osyA!111')
    text = values[0] + KeyInputs.ENTER\
        + values[1] + KeyInputs.ENTER\
        + values[1] + KeyInputs.ENTER\
        + "\r"
    result = ask_with_patched_input(AuthView.prompt_manager, text)
    assert result == values


def test_prompt_confirm_testdata():
    text = "n" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(AuthView.prompt_confirm_testdata, text)
    assert not result
