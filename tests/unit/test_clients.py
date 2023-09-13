from epicevents.models.entities import Department, Commercial, Client


class TestClients:

    def initdb(self, db_session):
        commercial_dpt = Department(name='commercial department')
        db_session.add(commercial_dpt)

    def add_commercials(self, db_session):
        d = Department.find_by_name(db_session, 'commercial department')
        e1 = Commercial(username='Yuka', department_id=d.id)
        e2 = Commercial(username='Esumi', department_id=d.id)
        e3 = Commercial(username='Morihei', department_id=d.id)
        db_session.add_all([e1, e2, e3])

    def add_clients_to_yuka(self, db_session):
        e = Commercial.find_by_username(db_session, 'Yuka')
        c1 = Client(full_name='Client 1', commercial_id=e.id)
        c2 = Client(full_name='Client 2', commercial_id=e.id)
        c3 = Client(full_name='Client 3', commercial_id=e.id)
        db_session.add_all([c1, c2, c3])

    def test_list_clients(self, db_session):
        self.initdb(db_session)
        self.add_commercials(db_session)
        self.add_clients_to_yuka(db_session)
        e = Commercial.find_by_username(db_session, 'Yuka')
        print('---------------> ' + str(e))
        print('---------------> ' + str(e.clients))
        assert str(e.clients[0]) == 'Client Client 1'
        assert str(e.clients[1]) == 'Client Client 2'
        assert str(e.clients[2]) == 'Client Client 3'
