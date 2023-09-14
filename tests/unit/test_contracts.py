from epicevents.models.entities import (
    Department, Commercial,
    Client, Contract, Paiement
    )


class TestContracts:

    def initdb(self, db_session):
        commercial_dpt = Department(name='commercial department')
        db_session.add(commercial_dpt)

    def add_commercials(self, db_session):
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Commercial(username='Yuka', department_id=d.id)
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
        p = Paiement(amount=100, contract_id=c.id)
        db_session.add(p)

    def test_list_contracts(self, db_session):
        self.initdb(db_session)
        self.add_commercials(db_session)
        self.add_clients_to_yuka(db_session)
        self.add_contracts_on_client1(db_session)
        self.add_contracts_on_client2(db_session)
        assert db_session.query(Contract).count() == 3
        e = Commercial.find_by_username(db_session, 'Yuka')
        contracts = e.get_contracts()
        assert str(contracts[0]) == 'Contract 1 for the client 1'
        assert str(contracts[1]) == 'Contract 2 for the client 1'
        assert str(contracts[2]) == 'Contract 3 for the client 2'

    def test_paiements(self, db_session):
        self.initdb(db_session)
        self.add_commercials(db_session)
        self.add_clients_to_yuka(db_session)
        self.add_contracts_on_client2(db_session)
        self.add_paiement_on_contract3(db_session)
        c = Contract.find_by_ref(db_session, '2023091303')
        assert c.outstanding() == 29900
