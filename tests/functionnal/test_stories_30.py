import epicevent
from ..mock_functions import MockFunction
from epicevents.views.client_views import ClientView
from epicevents.views.employee_views import EmployeeView


def test_story_30(runner, epicstories_yuka):

    def newdata():
        return {
            'full_name': 'YukaCliNew', 'email': 'yukaclinew@epic.co',
            'phone': '222-2222-2222',
            'company_name': 'NewCompagny Yuka'}

    epicstories_yuka.setattr(
        ClientView,
        'prompt_data_client', newdata)

    epicstories_yuka.setattr(
       ClientView, 'prompt_client', MockFunction.mock_clientyuka)

    epicstories_yuka.setattr(
            EmployeeView,
            'prompt_confirm_commercial',
            MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['client', 'update'])
    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    result = runner.invoke(epicevent.main, ['client', 'list'])
    expected = "YukaCliNew  │ yukaclinew@epic.co   │ 222-2222-2222 │ "
    expected += "NewCompagny Yuka            │ Yuka"
    assert expected in result.output
