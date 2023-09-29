from sqlalchemy.exc import IntegrityError
from epicevents.views.data_views import DataView
from epicevents.models.entities import Client, Contract, Paiement


class ContractBase:

    """ Manage crud operations on Contract base """

    def __init__(self, session) -> None:
        self.session = session

    def get_states(self):
        states = Contract.CONTRACT_STATES
        result = [s[1] for s in states]
        return result

    def get_state(self, ref):
        c = Contract.find_by_ref(self.session, ref)
        return c.state.code

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

    def get_active_contracts(self):
        return Contract.getallactive(self.session)

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

    def add_paiement(self, ref_contract, data):
        c = Contract.find_by_ref(self.session, ref_contract)
        if int(data['amount']) > c.outstanding:
            DataView.display_error_contract_amount()
        else:
            p = Paiement(
                ref=data['ref'], amount=data['amount'], contract_id=c.id)

            try:
                self.session.add(p)
                self.session.commit()
                DataView.display_data_update()
            except IntegrityError:
                self.session.rollback()
                DataView.display_error_unique()

    def update(self, ref_contract, data):
        c = Contract.find_by_ref(self.session, ref_contract)
        c.ref = data['ref']
        c.description = data['description']
        c.total_amount = data['total_amount']
        try:
            self.session.add(c)
            self.session.commit()
            DataView.display_data_update()
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()
