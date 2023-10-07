import epicevent

from ..mock_functions import MockFunction
from epicevents.views.employee_views import EmployeeView


def test_story_25(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_confirm_task', MockFunction.mock_prompt_confirm_yes)

    epicstories.setattr(
        EmployeeView,
        'prompt_select_task', MockFunction.mock_choice1
    )

    result = runner.invoke(epicevent.main, ['employee', 'terminate-task'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    result = runner.invoke(epicevent.main, ['employee', 'tasks'])

    assert "Mes tâches à réaliser" in result.output
    assert "Task to terminate" not in result.output
