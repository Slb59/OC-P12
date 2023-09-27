import pytest
from epicevents.models.entities import (
    Department, Commercial,
    Client, Contract, Paiement,
    ContractsAreActived
    )


class TestContracts:

    def initdb(self, db_session):
        commercial_dpt = Department(name='commercial department')
        db_session.add(commercial_dpt)

    def add_yuka(self, db_session):
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Commercial(username='Yuka', department_id=d.id, role='C')
        db_session.add(e1)

    def add_clients_to_yuka(self, db_session):
        e = Commercial.find_by_username(db_session, 'Yuka')
        c1 = Client(full_name='Client 1', commercial_id=e.id)
        c2 = Client(full_name='Client 2', commercial_id=e.id)
        db_session.add_all([c1, c2])

    def add_contracts_on_client1(self, db_session):
        c = Client.find_by_name(db_session, 'Client 1')
        contract_description = "Contract 1 for the client 1"
        contract1 = Contract(
            ref='2023091301',
            description=contract_description,
            client_id=c.id,
            total_amount=10000
            )
        contract_description = "Contract 2 for the client 1"
        contract2 = Contract(
            ref='2023091302',
            description=contract_description,
            client_id=c.id,
            total_amount=15000
            )
        db_session.add_all([contract1, contract2])

    def add_contracts_on_client2(self, db_session):
        c = Client.find_by_name(db_session, 'Client 2')
        contract_description = "Contract 3 for the client 2"
        contract = Contract(
            ref='2023091303',
            description=contract_description,
            client_id=c.id,
            total_amount=30000
            )
        db_session.add(contract)

    def add_paiement_on_contract3(self, db_session):
        c = Contract.find_by_ref(db_session, '2023091303')
        p = Paiement(amount=100, contract_id=c.id, ref='202309140833')
        db_session.add(p)

    def test_list_contracts(self, db_session):
        # given
        self.initdb(db_session)
        self.add_yuka(db_session)
        self.add_clients_to_yuka(db_session)
        self.add_contracts_on_client1(db_session)
        # when
        self.add_contracts_on_client2(db_session)
        # then
        assert db_session.query(Contract).count() == 3
        e = Commercial.find_by_username(db_session, 'Yuka')
        assert str(e.contracts[0]) == 'Contract 1 for the client 1'
        assert str(e.contracts[1]) == 'Contract 2 for the client 1'
        assert str(e.contracts[2]) == 'Contract 3 for the client 2'

    def test_paiements(self, db_session):
        # given
        self.initdb(db_session)
        self.add_yuka(db_session)
        self.add_clients_to_yuka(db_session)
        self.add_contracts_on_client2(db_session)
        # when
        self.add_paiement_on_contract3(db_session)
        # then
        c = Contract.find_by_ref(db_session, '2023091303')
        assert c.outstanding == 29900

    def test_update_commercial_role_without_contract(self, db_session):
        # given
        self.initdb(db_session)
        self.add_yuka(db_session)
        e = Commercial.find_by_username(db_session, 'Yuka')
        # when
        e.update_role('S')
        # then
        assert e.role == 'S'

    def test_update_commercial_role_with_activecontract(self, db_session):
        # given
        self.initdb(db_session)
        self.add_yuka(db_session)
        e = Commercial.find_by_username(db_session, 'Yuka')
        # when
        self.add_clients_to_yuka(db_session)
        self.add_contracts_on_client1(db_session)
        with pytest.raises(Exception) as e_info:
            e.update_role('S')
        assert e_info.type is ContractsAreActived

    def test_update_commercial_role_with_inactivecontract(self, db_session):
        # given
        self.initdb(db_session)
        self.add_yuka(db_session)
        e = Commercial.find_by_username(db_session, 'Yuka')
        # when
        self.add_clients_to_yuka(db_session)
        c = Client.find_by_name(db_session, 'Client 1')
        contract_description = "Contract 1 for the client 1"
        contract1 = Contract(
            ref='2023091301',
            description=contract_description,
            client_id=c.id,
            total_amount=10000
            )
        db_session.add(contract1)
        c = Contract.find_by_ref(db_session, '2023091301')
        c.state = 'X'
        db_session.add(c)
        # and when
        e.update_role('S')
        # then
        assert e.role == 'S'
