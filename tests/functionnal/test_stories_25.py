import epicevent

from ..mock_functions import MockFunction
from epicevents.employee.employee_views import EmployeeView
from epicevents.views.auth_views import AuthView


def test_story_25(epicstories):
    """ an employee terminate a task"""
    (mp, runner) = epicstories
    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        EmployeeView,
        'prompt_confirm_task', MockFunction.mock_prompt_confirm_yes)

    mp.setattr(
        EmployeeView,
        'prompt_select_task', MockFunction.mock_choice1
    )

    result = runner.invoke(epicevent.main, ['employee', 'terminate-task'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    result = runner.invoke(epicevent.main, ['employee', 'tasks'])

    assert "Mes tâches à réaliser" in result.output
    assert "Task to terminate" not in result.output
