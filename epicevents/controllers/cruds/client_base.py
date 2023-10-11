from sqlalchemy.exc import IntegrityError
from epicevents.views.data_views import DataView
from epicevents.models.entities import (
    Commercial, Client
)


class ClientBase:

    """ Manage crud operations on Client base """

    def __init__(self, session) -> None:
        self.session = session

    def get(self, client_name) -> Client:
        """find a client in the database

        Args:
            client_name (str): Client.full_name

        Returns:
            Client: instance of Client
        """
        return Client.find_by_name(self.session, client_name)

    def get_clients(self, commercial_name='') -> list:
        """ find all clients

        Args:
            commercial_name (str, optional): filter list for a commercial_name.
            Defaults to ''.

        Returns:
            list: list of instance of Client
        """
        if commercial_name:
            e = Commercial.find_by_username(self.session, commercial_name)
            result = e.clients
        else:
            result = Client.getall(self.session)
        return result

    def update_commercial(self, client_name, commercial_name) -> None:
        """ update the commercial of a client

        Args:
            client_name (_type_): _description_
            cname (_type_): _description_
        """
        c = Client.find_by_name(self.session, client_name)
        e = Commercial.find_by_username(self.session, commercial_name)
        c.commercial_id = e.id
        self.session.add(c)
        self.session.commit()
        DataView.display_data_update()

    def create(self, commercial_name, data) -> None:
        """create a new client associate with a commercial

        Args:
            commercial_name (str): name of the commercial
            data (dict): exemple : {
            'full_name': 'client-test', 'email': 'test@test.com',
            'phone': '0202020202', 'company_name': 'company_name'}
        """
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

    def update(self, client_name, data) -> str:
        """update the client data

        Args:
            client_name (str): Client.full_name
            data (dict): exemple : {
            'full_name': 'client-test', 'email': 'test@test.com',
            'phone': '0202020202', 'company_name': 'company_name'}

        Returns:
            str: new client name
        """
        c = Client.find_by_name(self.session, client_name)
        c.full_name = data['full_name']\
            if data['full_name'] else client_name
        c.email = data['email']\
            if data['email'] else c.email
        c.phone = data['phone']\
            if data['phone'] else c.phone
        c.company_name = data['company_name']\
            if data['company_name'] else c.company_name
        try:
            self.session.add(c)
            self.session.commit()
            DataView.display_data_update()
            return c.full_name
        except IntegrityError:
            self.session.rollback()
            DataView.display_error_unique()
            return client_name
