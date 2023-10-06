
import epicevent

from ..mock_functions import MockFunction

from epicevents.views.employee_views import EmployeeView


def test_story_10(runner, epicstories):

    epicstories.setattr(
        EmployeeView,
        'prompt_data_employee', MockFunction.mock_prompt_data_employee)

    result = runner.invoke(epicevent.main, ['employee', 'create'])
    result2 = runner.invoke(epicevent.main, ['employee', 'list'])

    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output
    assert "NewUser" in result2.output
