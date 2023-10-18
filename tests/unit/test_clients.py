from epicevents.models.entities import Commercial


class TestClients:

    def test_list_clients(
            self,
            db_session,
            yuka, add_3_clients_to_yuka):
        # GIVEN database include a commercial departement
        # GIVEN database include Yuka as commercial
        # GIGEN we add 3 clients to Yuka
        # WHEN ask for Yuka instance
        e = Commercial.find_by_username(db_session, 'Yuka')
        # THEN we can access Yuka clients
        assert str(e.clients[0]) == 'Client Client 1'
        assert str(e.clients[1]) == 'Client Client 2'
        assert str(e.clients[2]) == 'Client Client 3'
