from epicevents.views.data_views import DataView
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

    def update_commercial(self, client_name, cname):
        c = Client.find_by_name(self.session, client_name)
        e = Commercial.find_by_username(self.session, cname)
        c.commercial_id = e.id
        self.session.add(c)
        DataView.display_data_update()
