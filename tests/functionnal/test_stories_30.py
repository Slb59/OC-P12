import epicevent
from ..mock_functions import MockFunction
from epicevents.client.client_views import ClientView
from epicevents.employee.employee_views import EmployeeView
from epicevents.views.auth_views import AuthView


def test_story_30(epicstories):
    (mp, runner) = epicstories

    def newdata():
        return {
            'full_name': 'YukaCliNew', 'email': 'yukaclinew@epic.co',
            'phone': '222-2222-2222',
            'company_name': 'NewCompagny Yuka'}

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_yuka)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ClientView,
        'prompt_data_client', newdata)

    mp.setattr(
       ClientView, 'prompt_client', MockFunction.mock_clientyuka)

    mp.setattr(
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
