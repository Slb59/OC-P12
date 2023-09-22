from epicevents.models.entities import (
    Department, Commercial, Client,
    Contract, Event, EventType)
from epicevents.views.console import console
from epicevents.views.list_views import (
    display_list_clients,
    display_list_contracts,
    display_list_events
)


def initdb(db_session):
    commercial_dpt = Department(name='commercial department')
    db_session.add(commercial_dpt)
    d = Department.find_by_name(db_session, 'commercial department')
    e1 = Commercial(username='Yuka', department_id=d.id, role='C')
    db_session.add(e1)
    e1 = Commercial.find_by_username(db_session, 'Yuka')
    for i in range(3):
        c = Client(
            full_name=f'Client n°{i+1}',
            email=f'Client{i+1}@example.com',
            commercial_id=e1.id
        )
        db_session.add(c)


def add_contracts(db_session):
    c = Client.find_by_name(db_session, 'Client n°1')
    for i in range(3):
        contract_description = f"Contract {i+1} for {c.full_name}"
        state = 'C'
        new_contract = Contract(
            ref='Ref' + str(i+1),
            description=contract_description,
            client_id=c.id,
            total_amount=1000,
            state=state
            )
        db_session.add(new_contract)


def add_events(db_session):
    c = Contract.find_by_ref(db_session, 'Ref1')
    event_type1 = EventType(title='conference')
    db_session.add(event_type1)
    t = EventType.find_by_title(db_session, 'conference')
    for i in range(3):
        e = Event(
            title=f'Event{i+1}',
            contract_id=c.id,
            date_started='2023-09-14 15:00:00.000000',
            date_ended='2023-09-24 18:00:00.000000',
            type_id=t.id
        )
        db_session.add(e)


def test_display_list_clients(db_session):
    # given
    initdb(db_session)
    # when
    with console.capture() as capture:
        display_list_clients(Client.getall(db_session), False)
    # then
    str_output = capture.get()
    assert "Liste des clients" in str_output
    assert "Client n°1" in str_output
    assert "Client n°2" in str_output
    assert "Client n°3" in str_output


def test_display_list_contracts(db_session):
    # given
    initdb(db_session)
    add_contracts(db_session)
    # when
    with console.capture() as capture:
        display_list_contracts(Contract.getall(db_session), False)
    # then
    str_output = capture.get()
    assert "Liste des contracts" in str_output
    assert "ref1" in str_output.lower()
    assert "ref2" in str_output.lower()
    assert "ref3" in str_output.lower()


def test_display_list_events(db_session):
    # given
    initdb(db_session)
    c = Client.find_by_name(db_session, 'Client n°1')
    new_contract = Contract(
            ref='Ref1',
            description='Ref1',
            client_id=c.id,
            total_amount=1000)
    db_session.add(new_contract)
    add_events(db_session)
    # when
    with console.capture() as capture:
        display_list_events(Event.getall(db_session), False)
    # then
    str_output = capture.get()
    assert "Liste des évènements" in str_output
    assert "Event1" in str_output
    assert "Event2" in str_output
    assert "Event3" in str_output
