from epicevents.views.console import console
from epicevents.views.event_views import EventView
from .utils import (
    KeyInputs, ask_with_patched_select)


def test_display_no_event():
    expected = "Il n'y a pas d'évènement pour ces critères\n"
    with console.capture() as capture:
        EventView.display_no_event()
    out = capture.get()
    assert out == expected


def test_prompt_type():
    text = KeyInputs.DOWN + KeyInputs.ENTER + KeyInputs.ENTER + "\r"
    choice = ['show', 'seminar', 'autre']
    result = ask_with_patched_select(
        EventView.prompt_type, text, choice)
    assert result == "seminar"
