from epicevents.views.console import console
from epicevents.views.business_views.event_views import EventView
from ..utils import (
    KeyInputs, ask_with_patched_input)


def test_display_no_event():
    expected = "Il n'y a pas d'évènement pour ces critères\n"
    with console.capture() as capture:
        EventView.display_no_event()
    out = capture.get()
    assert out == expected


def test_prompt_data_event():
    values = {
        'title': 'title',
        'description': 'description',
        'location': 'location', 'attendees': '200',
        'date_started': '01/10/2023', 'date_ended': '30/10/2023'}
    text = values['title'] + KeyInputs.ENTER\
        + values['description'] + KeyInputs.ENTER\
        + values['location'] + KeyInputs.ENTER\
        + values['attendees'] + KeyInputs.ENTER\
        + values['date_started'] + KeyInputs.ENTER\
        + values['date_ended'] + KeyInputs.ENTER\
        + "\r"
    result = ask_with_patched_input(
        EventView.prompt_data_event, text)
    assert result == values


def test_select_event():
    expected = "Choix de l'évènement:"
    assert EventView.select_event() == expected


def test_select_type_event():
    expected = "Type d'évènement:"
    assert EventView.select_type_event() == expected


def test_workflow_affect():
    expected = "Vous avez été affecté à l'évènement nom_event"
    assert EventView.workflow_affect("nom_event") == expected


def test_workflow_ask_affect():
    expected = "Affecter un support pour l'évènement nom_event"
    assert EventView.workflow_ask_affect("nom_event") == expected


def test_no_event():
    expected = "Il n'y a pas d'évènement sélectionnable"
    assert EventView.no_event() == expected


def test_no_support():
    expected = "-- sans support --"
    assert EventView.no_support() == expected


def test_prompt_rapport():
    text = "Mon rapport" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        EventView.prompt_rapport, text)
    assert "Mon rapport" == result
