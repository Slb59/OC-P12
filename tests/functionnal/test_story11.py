import epicevent

from ..mock_functions import MockFunction
from epicevents.views.employee_views import EmployeeView


def test_story_11(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_role', MockFunction.mock_role_manager)
    epicstories.setattr(
        EmployeeView,
        'prompt_employee', MockFunction.mock_employee_support)

    result = runner.invoke(epicevent.main, ['employee', 'update-role'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])
    result3 = runner.invoke(epicevent.main, ['employee', 'tasks'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "Aritomo     │       │ Manager" in result2.output
    assert "Affecter un support pour l'évènement Aritomo" in result3.output
