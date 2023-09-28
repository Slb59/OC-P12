from sqlalchemy.exc import IntegrityError
from epicevents.views.data_views import DataView
from epicevents.models.entities import Client, Contract


class ContractBase:

    """ Manage crud operations on Contract base """

    def __init__(self, session) -> None:
        self.session = session

    def get_states(self):
        states = Contract.CONTRACT_STATES
        result = [s[1] for s in states]
        return result

    def get_contracts(
            self, commercial_name=None,
            client_name=None,
            state_value=None):
        state = None
        if state_value:
            states = Contract.CONTRACT_STATES
            for s in states:
                if state_value in s:
                    state = s[0]
        return Contract.find_by_selection(
            self.session, commercial_name, client_name, state)

    def create(self, client_name, data):
        c = Client.find_by_name(self.session, client_name)
        contract = Contract(
            ref=data['ref'],
            description=data['description'],
            total_amount=int(data['total_amount']),
            client_id=c.id
        )
        try:
            self.session.add(contract)
            self.session.commit()
            DataView.display_data_update()
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()
