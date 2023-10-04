from epicevents.views.console import console
from epicevents.views.event_views import EventView


def test_display_no_event():
    expected = "Il n'y a pas d'évènement pour ces critères\n"
    with console.capture() as capture:
        EventView.display_no_event()
    out = capture.get()
    assert out == expected
