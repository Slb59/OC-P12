from epicevents.models.entities import Event, Support, Contract, EventType
from epicevents.views.data_views import DataView


class EventBase:

    """ Manage crud operations on Event base """

    def __init__(self, session) -> None:
        self.session = session

    def get_types(self) -> list:
        """List all of event type

        Returns:
            list: list of instance of EventType
        """
        return EventType.getall(self.session)

    def get_events(
            self,
            commercial_name=None,
            client_name=None,
            contract_ref=None,
            support_name=None,
            state_code=None):
        if support_name == '-- sans support --':
            support_name = 'None'
        return Event.find_by_selection(
            self.session, commercial_name, client_name,
            contract_ref, support_name, state_code
        )

    def update(self, contract_ref, event_title, support):
        c = Contract.find_by_ref(self.session, contract_ref)
        e = Event.find_by_title(self.session, c.id, event_title)
        s = Support.find_by_username(self.session, support)
        e.support_id = s.id
        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()

    def create(self, contract_ref, event_type, data):
        c = Contract.find_by_ref(self.session, contract_ref)
        type = EventType.find_by_title(self.session, event_type)
        e = Event(
            title=data['title'], description=data['description'],
            location=data['location'], attendees=data['attendees'],
            date_started=data['date_started'], date_ended=data['date_ended'],
            contract_id=c.id, type_id=type.id
        )
        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()

    def terminate(self, event_ref, report_text):
        (contract_ref, event_title) = event_ref.split('|')
        c = Contract.find_by_ref(self.session, contract_ref)
        e = Event.find_by_title(self.session, c.id, event_title)
        e.report = report_text
        e.state = 'C'
        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()

    def cancel(self, event_ref):
        (contract_ref, event_title) = event_ref.split('|')
        c = Contract.find_by_ref(self.session, contract_ref)
        e = Event.find_by_title(self.session, c.id, event_title)
        e.state = 'X'
        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()
