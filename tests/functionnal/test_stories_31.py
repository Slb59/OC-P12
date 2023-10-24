import epicevent
from ..mock_functions import MockFunction
from epicevents.contract.contract_views import ContractView
from epicevents.event.event_views import EventView
from epicevents.employee.employee_views import EmployeeView
from epicevents.client.client_views import ClientView
from epicevents.views.auth_views import AuthView


def test_story_31(epicstories):
    """ a commercial create a new event """
    (mp, runner) = epicstories

    def mock_type_select(*args, **kwargs):
        return 'conference'

    def mock_data_event(*args, **kwargs):
        return {
            'title': 'EVYukaContrat', 'description': 'EVYukaContrat',
            'location': 'France', 'attendees': '10',
            'date_started': '01/10/2023', 'date_ended': '30/10/2023'}

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_yuka)
    runner.invoke(epicevent.main, ['login'])

    mp.setattr(
        ContractView,
        'prompt_select_contract', MockFunction.mock_contract1)

    mp.setattr(
        EventView,
        'prompt_select_type', mock_type_select)

    mp.setattr(
        EventView, 'prompt_data_event', mock_data_event)

    result = runner.invoke(epicevent.main, ['event', 'create'])
    assert not result.exception
    assert "Vos modifications ont été enregistrées" in result.output

    mp.setattr(
        EmployeeView, 'prompt_confirm_commercial',
        MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ClientView,
            'prompt_confirm_client',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            ContractView,
            'prompt_confirm_contract',
            MockFunction.mock_prompt_confirm_no)
    mp.setattr(
            EmployeeView,
            'prompt_confirm_support',
            MockFunction.mock_prompt_confirm_no)

    result = runner.invoke(epicevent.main, ['event', 'list'])
    assert not result.exception
    expected = "YukaCli     │ contrat1                  │ conference │ "
    expected += "EVYukaContrat  │ "
    expected += "France     │ 10               │ du 01/10/2023-00h00 │ "
    expected += "A venir │ Yuka"
    assert expected in result.output

    mp.setattr(
        AuthView, 'prompt_login', MockFunction.mock_login_osynia)
    runner.invoke(epicevent.main, ['login'])
    result = runner.invoke(epicevent.main, ['employee', 'tasks'])
    expected = "Affecter un support pour l'évènement EVYukaContrat"
    assert expected in result.output
