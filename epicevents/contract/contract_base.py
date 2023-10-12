from sqlalchemy.exc import IntegrityError
from epicevents.views.data_views import DataView
from epicevents.models.entities import (
    Client, Contract, Paiement)


class ContractBase:

    """ Manage crud operations on Contract base """

    def __init__(self, session) -> None:
        self.session = session

    def get(self, ref) -> Contract:
        """ give a contrat instance for the ref

        Args:
            ref (str): a ref of a contract

        Returns:
            Contrat: an instance of contract
        """
        return Contract.find_by_ref(self.session, ref)

    def get_states(self) -> list:
        """ Give the list of state names

        Returns:
            list: list of the state names
        """
        states = Contract.CONTRACT_STATES
        result = [s[1] for s in states]
        return result

    def get_state(self, ref) -> str:
        """ give the code state of a contract

        Args:
            ref (str): ref of the contract

        Returns:
            str: code of the state
        """
        c = Contract.find_by_ref(self.session, ref)
        return c.state.code

    def get_contracts(
            self, commercial_name=None,
            client_name=None,
            state_value=None) -> list:
        """Give a list of contracts wich match with the selection

        Args:
            commercial_name (str, optional): the commercial username.
            Defaults to None.
            client_name (str, optional): the client full_name.
            Defaults to None.
            state_value (str, optional): the state name. Defaults to None.

        Returns:
            list: a list of instance of Contract
        """
        state = None
        if state_value:
            states = Contract.CONTRACT_STATES
            for s in states:
                if state_value in s:
                    state = s[0]
        return Contract.find_by_selection(
            self.session, commercial_name, client_name, state)

    def get_active_contracts(self) -> list:
        """ Give the list of active contract
        a contract is active if state in (C = create,S = signed)

        Returns:
            list: list of instance of Contract
        """
        return Contract.getallactive(self.session)

    def create(self, client_name, data) -> None:
        """ create a new contract for the client_name in the database

        Args:
            client_name (str): client full_name
            data (dict): example:
            {'ref': ref, 'description': description,
                'total_amount': total_amount}
        """
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

    def add_paiement(self, ref_contract, data) -> None:
        """ create a new paiement for the contract in the database

        Args:
            ref_contract (str): ref of the contract
            data (dict): example:
            {'ref': ref, 'amount': amount}
        """
        c = Contract.find_by_ref(self.session, ref_contract)
        if int(data['amount']) > c.outstanding:
            DataView.display_error_contract_amount()
        else:
            p = Paiement(
                ref=data['ref'], amount=data['amount'], contract_id=c.id)
            if int(data['amount']) == c.outstanding:
                c.state = 'B'
                self.session.add(c)
            try:
                self.session.add(p)
                self.session.commit()
                DataView.display_data_update()
            except IntegrityError:
                self.session.rollback()
                DataView.display_error_unique()

    def update(self, ref_contract, data) -> str:
        """ update the contrat ref_contract whith the data given

        Args:
            ref_contract (str): ref of the contract
            data (dict): example:
            {'ref': ref, 'description': description,
                'total_amount': total_amount}
        Returns:
            str: the new ref contract
        """
        c = Contract.find_by_ref(self.session, ref_contract)
        c.ref = data['ref']\
            if data['ref'] else ref_contract
        c.description = data['description']\
            if data['description'] else c.description
        c.total_amount = data['total_amount']\
            if data['total_amount'] else c.total_amount
        try:
            self.session.add(c)
            self.session.commit()
            DataView.display_data_update()
            return c.ref
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()
            return ref_contract

    def cancel(self, ref_contract) -> None:
        """ update the state of the contract to X=Cancel

        Args:
            ref_contract (str): ref of the contract
        """
        c = Contract.find_by_ref(self.session, ref_contract)
        c.state = 'X'
        self.session.add(c)
        self.session.commit()
        DataView.display_data_update()

    def signed(self, ref_contract) -> None:
        """
            update the state of the contract to S=Signed
        Args:
            ref_contract (str): ref of the contract
        """
        c = Contract.find_by_ref(self.session, ref_contract)
        c.state = 'S'
        self.session.add(c)
        self.session.commit()
        DataView.display_data_update()
