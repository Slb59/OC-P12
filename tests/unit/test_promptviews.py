import questionary
from prompt_toolkit.output import DummyOutput
from .utils import KeyInputs, execute_with_input_pipe
from .utils import feed_cli_with_input
from epicevents.views.prompt_views import PromptView


def ask_with_patched_input(q, text):
    def run(inp):
        inp.send_text(text)
        return q(input=inp, output=DummyOutput())
    return execute_with_input_pipe(run)


def ask_with_patched_select(q, text, choice):
    def run(inp):
        inp.send_text(text)
        result = q(choice, input=inp, output=DummyOutput())
        return result
    return execute_with_input_pipe(run)


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
        PromptView.prompt_confirm_commercial, text)
    assert result


def test_prompt_confirm_client():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_client, text)
    assert result


def test_prompt_confirm_statut():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_statut, text)
    assert result


def test_prompt_confirm_contract():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_contract, text)
    assert result


def test_prompt_confirm_support():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_support, text)
    assert result


def test_prompt_confirm_task():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_task, text)
    assert result


def test_prompt_confirm_profil():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        PromptView.prompt_confirm_profil, text)
    assert result


def test_prompt_client():
    text = KeyInputs.DOWN + KeyInputs.ENTER + KeyInputs.ENTER + "\r"
    choice = ['Alphonse', 'Dominique', 'Robert']
    result = ask_with_patched_select(
        PromptView.prompt_client, text, choice)
    assert result == "Dominique"