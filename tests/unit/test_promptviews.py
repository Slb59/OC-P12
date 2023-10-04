import questionary
from .utils import (
    KeyInputs,
    feed_cli_with_input, ask_with_patched_input,
    ask_with_patched_select
)
from epicevents.views.prompt_views import PromptView
from epicevents.views.employee_views import EmployeeView
from epicevents.views.client_views import ClientView


def test_confirm_enter_default_yes():
    message = "Foo message"
    text = KeyInputs.ENTER + "\r"
    result, cli = feed_cli_with_input("confirm", message, text)
    assert result is True


def ask_pystyle(**kwargs):
    return questionary.confirm(
        "Do you want to continue?", default=True, **kwargs
    ).ask()


def test_confirm_example():
    text = "n" + KeyInputs.ENTER + "\r"
    result_py = ask_with_patched_input(ask_pystyle, text)
    assert not result_py


def test_prompt_confirm_commercial():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        EmployeeView.prompt_confirm_commercial, text)
    assert result


def test_prompt_confirm_client():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        ClientView.prompt_confirm_client, text)
    assert result


def test_prompt_confirm_statut():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_statut, text)
    assert result


def test_prompt_confirm_support():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        EmployeeView.prompt_confirm_support, text)
    assert result


def test_prompt_confirm_task():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        EmployeeView.prompt_confirm_task, text)
    assert result


def test_prompt_confirm_profil():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        EmployeeView.prompt_confirm_profil, text)
    assert result


def test_prompt_client():
    text = KeyInputs.DOWN + KeyInputs.ENTER + KeyInputs.ENTER + "\r"
    choice = ['Alphonse', 'Dominique', 'Robert']
    result = ask_with_patched_select(
        ClientView.prompt_client, text, choice)
    assert result == "Dominique"
