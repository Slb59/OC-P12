import asyncio
from prompt_toolkit.output import DummyOutput
from prompt_toolkit.input.defaults import create_pipe_input
from questionary.prompts import prompt_by_name
from questionary.utils import is_prompt_toolkit_3


class KeyInputs:
    DOWN = "\x1b[B"
    UP = "\x1b[A"
    LEFT = "\x1b[D"
    RIGHT = "\x1b[C"
    ENTER = "\r"
    ESCAPE = "\x1b"
    CONTROLC = "\x03"
    CONTROLN = "\x0e"
    CONTROLP = "\x10"
    BACK = "\x7f"
    SPACE = " "
    TAB = "\x09"
    ONE = "1"
    TWO = "2"
    THREE = "3"


def execute_with_input_pipe(func):
    with create_pipe_input() as inp:
        return func(inp)


# from prompt_toolkit.input import create_pipe_input
# from prompt_toolkit.application import AppSession, create_app_session
# from prompt_toolkit.output import DummyOutput

# input = create_pipe_input()
# # Create an alternative input device, similar to StringIO.
# input.send_text("hello\n")

# with create_app_session(input=input, output=DummyOutput()):
#     #  run your application here. It will by default
# take the input/output objects from the AppSession.

def feed_cli_with_input(_type, message, texts, sleep_time=1, **kwargs):
    """
    Create a Prompt, feed it with the given user input and return the CLI
    object.

    You an provide multiple texts, the feeder will async sleep for `sleep_time`

    This returns a (result, Application) tuple.
    """

    if not isinstance(texts, list):
        texts = [texts]

    def _create_input(inp):
        prompter = prompt_by_name(_type)
        application = prompter(
            message, input=inp, output=DummyOutput(), **kwargs)
        if is_prompt_toolkit_3():
            loop = asyncio.new_event_loop()
            future_result = loop.create_task(application.unsafe_ask_async())

            for i, text in enumerate(texts):
                # noinspection PyUnresolvedReferences
                inp.send_text(text)

                if i != len(texts) - 1:
                    loop.run_until_complete(asyncio.sleep(sleep_time))
            result = loop.run_until_complete(future_result)
        else:
            for text in texts:
                inp.send_text(text)
            result = application.unsafe_ask()
        return result, application

    return execute_with_input_pipe(_create_input)


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


def ask_with_patched_select_with_title(q, text, title, choice):
    def run(inp):
        inp.send_text(text)
        result = q(title, choice, input=inp, output=DummyOutput())
        return result
    return execute_with_input_pipe(run)
