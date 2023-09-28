from epicevents.models.entities import (
    Commercial, Client
)


class ClientBase:

    """ Manage crud operations on Client base """

    def __init__(self, session) -> None:
        self.session = session

    def get_clients(self, commercial_name=''):
        if commercial_name:
            e = Commercial.find_by_username(self.session, commercial_name)
            result = e.clients
        else:
            result = Client.getall(self.session)
        return result
