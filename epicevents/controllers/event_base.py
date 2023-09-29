from epicevents.models.entities import Event, Support, Contract
from epicevents.views.data_views import DataView


class EventBase:

    """ Manage crud operations on Event base """

    def __init__(self, session) -> None:
        self.session = session

    def get_events(
            self,
            commercial_name=None,
            client_name=None,
            contract_ref=None,
            support_name=None):
        if support_name == '-- sans support --':
            support_name = 'None'
        return Event.find_by_selection(
            self.session, commercial_name, client_name,
            contract_ref, support_name
        )

    def update(self, contract_ref, event, support):
        c = Contract.find_by_ref(self.session, contract_ref)
        e = Event.find_by_title(self.session, c.id, event)
        s = Support.find_by_username(self.session, support)
        e.support_id = s.id
        self.session.add(e)
        self.session.commit()
        DataView.display_data_update()
