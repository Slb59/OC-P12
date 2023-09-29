from sqlalchemy.exc import IntegrityError
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
        self.session.commit()
        DataView.display_data_update()

    def create(self, commercial_name, data):
        # data = {
        # 'full_name': 'client-test', 'email': 'test@test.com',
        # 'phone': '0202020202', 'company_name': 'company_name'}
        e = Commercial.find_by_username(self.session, commercial_name)
        c = Client(
            full_name=data['full_name'], email=data['email'],
            phone=data['phone'], company_name=data['company_name'],
            commercial_id=e.id)
        try:
            self.session.add(c)
            self.session.commit()
            DataView.display_data_update()
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()

    def update(self, client_name, data):
        c = Client.find_by_name(self.session, client_name)
        c.full_name = data['full_name']
        c.email = data['email']
        c.phone = data['phone']
        c.company_name = data['company_name']
        try:
            self.session.add(c)
            self.session.commit()
            DataView.display_data_update()
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()
