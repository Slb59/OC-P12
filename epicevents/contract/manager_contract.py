from epicevents.controllers.decorators import (
    is_authenticated, is_manager,
    sentry_activate
)
from epicevents.employee.manager_employee import EpicManagerEmployee
from epicevents.client.manager_client import EpicManagerClient

from epicevents.views.prompt_views import PromptView
from epicevents.contract.contract_views import ContractView
from epicevents.client.client_views import ClientView
from epicevents.views.menu_views import MenuView
from epicevents.views.data_views import DataView


class EpicManagerContract():

    def __init__(self, user, base):
        self.user = user
        self.epic = base
        self.controller_employee = EpicManagerEmployee(self.user, self.epic)
        self.controller_client = EpicManagerClient(self.user, self.epic)

    @sentry_activate
    @is_authenticated
    def list_of_contracts(self):
        state = None
        cname = self.controller_employee.choice_commercial()
        client = self.controller_client.choice_client(cname)
        # select a state
        result = PromptView.prompt_confirm_statut()
        if result:
            states = self.epic.dbcontracts.get_states()
            try:
                state = ContractView.prompt_select_statut(states)
            except KeyboardInterrupt:
                state = None
        # display list
        ContractView.display_list_contracts(
            self.epic.dbcontracts.get_contracts(cname, client, state))

    @sentry_activate
    @is_authenticated
    @is_manager
    def create_contract(self):
        clients = self.epic.dbclients.get_clients()
        enames = [c.full_name for c in clients]
        ename = ClientView.prompt_client(enames)
        try:
            data = ContractView.prompt_data_contract()
            self.epic.dbcontracts.create(ename, data)
            contract_ref = data['ref']
            text = f'Contrat {contract_ref} en attente de signature'
            self.epic.dbemployees.create_task(self.user.username, text)
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_manager
    def update_contract(self):
        """
            - ask to select a contract in a list of active contract
            - ask which operation todo
                - you can add a paiement then:
                    - ask data for paiement
                    - create paiement in database
                - you can modify the data then:
                    - display the data of actuel contract
                    - ask for new data
                    - update database
                    - display new data
                - you can signed a contrat
                - you can cancel a contract
        """
        contracts = self.epic.dbcontracts.get_active_contracts()
        refs = [c.ref for c in contracts]
        ref = ContractView.prompt_select_contract(refs)
        state = self.epic.dbcontracts.get_state(ref)
        try:
            choice = MenuView.menu_update_contract(state)
            match choice:
                case 1:
                    try:
                        data = ContractView.prompt_data_paiement()
                        self.epic.dbcontracts.add_paiement(ref, data)
                    except KeyboardInterrupt:
                        DataView.display_interupt()
                case 2:
                    try:
                        contract = self.epic.dbcontracts.get(ref)
                        ContractView.display_contract_info(contract)
                        data = ContractView.prompt_data_contract(
                            ref_required=False, mt_required=False)
                        newref = self.epic.dbcontracts.update(ref, data)
                        contract = self.epic.dbcontracts.get(newref)
                        ContractView.display_contract_info(contract)
                    except KeyboardInterrupt:
                        DataView.display_interupt()
                case 3:
                    self.epic.dbcontracts.signed(ref)
                    text = f'Creer les évènements du contrat {ref}'
                    contract = self.epic.dbcontracts.get(ref)
                    DataView.display_workflow()
                    self.epic.dbemployees.create_task(
                        contract.client.commercial.username, text)
                case 4:
                    self.epic.dbcontracts.cancel(ref)
        except KeyboardInterrupt:
            DataView.display_interupt()
