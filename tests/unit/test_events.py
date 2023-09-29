import logging
from epicevents.models.entities import (
    Department, Commercial, Support,
    Client, Contract, Event, EventType
    )


log = logging.getLogger()


class TestEvent:

    def initdb(self, db_session):
        commercial_dpt = Department(name='commercial department')
        support_dpt = Department(name='support department')
        db_session.add_all([commercial_dpt, support_dpt])
        event_type1 = EventType(title='conference')
        event_type2 = EventType(title='forum')
        event_type3 = EventType(title='show')
        event_type4 = EventType(title='seminar')
        db_session.add_all(
            [event_type1, event_type2, event_type3, event_type4]
            )

    def add_employees(self, db_session):
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Commercial(username='Yuka', department_id=d.id, role='C')
        db_session.add(e1)
        d = Department.find_by_name(db_session, 'support department')
        e1 = Support(username='Aritomo', department_id=d.id, role='S')
        e2 = Support(username='Michio', department_id=d.id, role='S')
        e3 = Support(username='Poemu', department_id=d.id, role='S')
        db_session.add_all([e1, e2, e3])

    def add_client_to_yuka(self, db_session):
        e = Commercial.find_by_username(db_session, 'Yuka')
        c = Client(full_name='Client 1', commercial_id=e.id)
        db_session.add(c)

    def add_contract_on_client(self, db_session):
        c = Client.find_by_name(db_session, 'Client 1')
        contract_description = "Contract 1 for the client 1"
        contract = Contract(
            ref='2023091301',
            description=contract_description,
            client_id=c.id,
            total_amount=10000
            )
        db_session.add(contract)

    def add_events_on_contract(self, db_session):
        c = Contract.find_by_ref(db_session, '2023091301')
        t = EventType.find_by_title(db_session, 'seminar')
        e1 = Event(title='seiminaire on contract 2023091301',
                   contract_id=c.id,
                   date_started='2023-09-14 15:00:00.000000',
                   date_ended='2023-09-24 18:00:00.000000',
                   type_id=t.id
                   )
        t = EventType.find_by_title(db_session, 'conference')
        e2 = Event(title='conference on contract 2023091301',
                   contract_id=c.id,
                   date_started='2023-09-14 09:00:00.000000',
                   date_ended='2023-09-14 18:00:00.000000',
                   type_id=t.id
                   )
        t = EventType.find_by_title(db_session, 'show')
        e3 = Event(title='show on contract 2023091301',
                   contract_id=c.id,
                   date_started='2023-09-20 08:00:00.000000',
                   date_ended='2023-09-21 18:00:00.000000',
                   type_id=t.id
                   )
        db_session.add_all([e1, e2, e3])

    def test_list_support(self, db_session):
        self.initdb(db_session)
        self.add_employees(db_session)
        d = Department.find_by_name(db_session, 'support department')
        assert len(d.employees) == 3

    def test_list_events_from_contract(self, db_session):
        self.initdb(db_session)
        self.add_employees(db_session)
        self.add_client_to_yuka(db_session)
        self.add_contract_on_client(db_session)
        self.add_events_on_contract(db_session)
        c = Contract.find_by_ref(db_session, '2023091301')
        assert len(c.events) == 3

    def test_list_events_from_support(self, db_session):
        self.initdb(db_session)
        self.add_employees(db_session)
        self.add_client_to_yuka(db_session)
        self.add_contract_on_client(db_session)
        c = Contract.find_by_ref(db_session, '2023091301')
        self.add_events_on_contract(db_session)
        event = Event.find_by_title(
            db_session, c.id, 'conference on contract 2023091301'
            )
        support = Support.find_by_username(db_session, 'Aritomo')
        event.support_id = support.id
        db_session.add(event)
        event = Event.find_by_title(
            db_session, c.id, 'show on contract 2023091301'
            )
        event.support_id = support.id
        assert len(support.events) == 2

    def test_list_events_no_support(self, db_session):
        self.initdb(db_session)
        self.add_employees(db_session)
        self.add_client_to_yuka(db_session)
        self.add_contract_on_client(db_session)
        c = Contract.find_by_ref(db_session, '2023091301')
        self.add_events_on_contract(db_session)
        events = Event.getall(db_session)
        assert len(events) == 3
        event = Event.find_by_title(
            db_session, c.id, 'conference on contract 2023091301'
            )
        support = Support.find_by_username(db_session, 'Aritomo')
        event.support_id = support.id
        db_session.add(event)
        events = Event.getall(db_session)
        for e in events:
            if e.support_id:
                log.debug(e.support.username)
            else:
                log.debug(f'{e.id} Pas de support')
        events = Event.find_by_selection(
            session=db_session,
            commercial=None, client=None, contract=None,
            support='Aritomo')
        log.debug(events)
        assert len(events) == 1
        events = Event.find_by_selection(
            session=db_session,
            commercial=None, client=None, contract=None,
            support='None')
        assert len(events) == 2
