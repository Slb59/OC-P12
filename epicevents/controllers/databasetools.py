import random
from datetime import datetime, timedelta, timezone
from random import randint
from psycopg2.errors import UniqueViolation
from .database import EpicDatabase
from epicevents.models.entities import (
    Client, Contract,
    Commercial, Support, Manager,
    Event, EventType,
    Task
)


class EpicDatabaseWithData(EpicDatabase):

    def first_initdb(self, username, password):
        super().first_initdb(username, password)
        self.create_a_test_database()

    def add_some_contracts(self):
        clients = Client.getall(self.session)
        for c in clients:
            nb_of_contracts = randint(0, 10)
            for i in range(nb_of_contracts):
                contract_description = f"Contract {i} for {c.full_name}"
                dt = datetime.now().strftime('%Y%m%d-%H%M%S:%f')
                state = random.choice(Contract.CONTRACT_STATES)[0]
                new_contract = Contract(
                    ref=f"{dt}-{randint(1000, 9999)}",
                    description=contract_description,
                    client_id=c.id,
                    total_amount=randint(500, 30000),
                    state=state
                    )
                self.session.add(new_contract)
                try:
                    self.session.commit()
                except UniqueViolation:
                    pass
        # create a special contract on client0
        client = Client.find_by_name(self.session, 'Client n°0')
        new_contract = Contract(
            ref="contrat1",
            description="contrat1",
            client_id=client.id,
            total_amount=3000,
            state='S'
        )
        self.session.add(new_contract)
        self.session.commit()

    def add_some_clients(self):
        self.dbemployees.add_employee('Morihei', 'moriH!111', 'Commercial')
        self.dbemployees.add_employee('Yuka', 'yuka!111', 'Commercial')
        e1 = Commercial.find_by_username(self.session, 'Yuka')
        self.dbemployees.add_employee('Esumi', 'esuM!111', 'Commercial')        
        e2 = Commercial.find_by_username(self.session, 'Esumi')
        company_names = ['League Computing',
                         'Valley Dressing',
                         'Jumpstart Travel',
                         'Social bleu-ciel',
                         'Restaurants de la citadelle']
        for i in range(20):
            c = Client(
                full_name=f'Client n°{i}',
                email=f'Client{i}@example.com',
                phone=f'{randint(10,80)}.{randint(100,800)}.{randint(10,80)}',
                company_name=random.choice(company_names),
                commercial_id=random.choice([e1.id, e2.id])
            )
            self.session.add(c)
        self.session.commit()

    def add_some_events(self):
        self.dbemployees.add_employee('Aritomo', 'ari!111', 'Support')
        self.dbemployees.add_employee('Michio', 'michi!111', 'Support')
        contracts = Contract.getall(self.session)
        locations = [
            'France',
            'Allemagne',
            'Chine',
            'angleterre',
            'Russie']
        for c in contracts:
            nb_of_events = randint(1, 10)
            for i in range(nb_of_events):
                title = f'Ev. n°{i}'
                description = f'Un énènement pour notre client {c.client}'
                nb = randint(10, 200)
                nbj_start = randint(1, 300)
                nbh_end = randint(1, 240)
                date_start = datetime.now(tz=timezone.utc)\
                    + timedelta(days=nbj_start)
                date_end = date_start\
                    + timedelta(hours=nbh_end)
                types = EventType.getall(self.session)
                ch_type = random.choice(types)
                state = random.choice(Event.EVENT_STATES)[0]
                somewhere = random.choice(locations)
                e = Event(
                    title=title, description=description,
                    attendees=nb, location=somewhere,
                    date_started=date_start,
                    date_ended=date_end,
                    state=state,
                    contract_id=c.id,
                    type_id=ch_type.id
                    )
                is_support = randint(0, 3)
                if is_support:
                    empls = Support.getall(self.session)
                    support = random.choice(empls)
                    e.support_id = support.id
                self.session.add(e)
        # create a specifique event on aritomo
        contract = contracts[0]
        nbj_start = randint(1, 300)
        nbh_end = randint(1, 240)
        date_start = datetime.now(tz=timezone.utc)\
            + timedelta(days=nbj_start)
        date_end = date_start\
            + timedelta(hours=nbh_end)
        types = EventType.getall(self.session)
        ch_type = random.choice(types)
        aritomo = Support.find_by_username(self.session, 'Aritomo')
        e = Event(
            title='Aritomo event', description='Aritomo event',
            attendees=10, location='somewhere',
            date_started=date_start,
            date_ended=date_end,
            contract_id=contract.id,
            type_id=ch_type.id,
            support_id=aritomo.id
            )
        self.session.add(e)
        self.session.commit()
        # create a specifique event on contrat 1
        contract = Contract.find_by_ref(self.session, 'contrat1')
        e = Event(
            title='contrat1 event', description='contrat1 event',
            attendees=10, location='somewhere',
            date_started=date_start,
            date_ended=date_end,
            contract_id=contract.id,
            type_id=ch_type.id,
        )
        self.session.add(e)
        self.session.commit()

    def add_some_tasks(self):
        managers = Manager.getall(self.session)
        ch_manager = managers[0]
        t = Task(
            description='Task to terminate',
            employee_id=ch_manager.id)
        self.session.add(t)
        for c in Client.find_without_contract(self.session):
            ch_manager = random.choice(managers)
            t = Task(
                description=f'Creer un contrat pour le client {c.full_name}',
                employee_id=ch_manager.id)
            self.session.add(t)        
        self.session.commit()


    def create_a_test_database(self):
        self.add_some_clients()
        self.add_some_contracts()
        self.add_some_events()
        self.add_some_tasks()
