import random

from epicevents.controllers.decorators import (
    is_authenticated, is_manager, is_support, is_commercial,
    sentry_activate
)
from epicevents.employee.manager_employee import EpicManagerEmployee
from epicevents.client.manager_client import EpicManagerClient

from epicevents.employee.employee_views import EmployeeView
from epicevents.contract.contract_views import ContractView
from epicevents.event.event_views import EventView
from epicevents.views.data_views import DataView


class EpicManagerEvent():

    def __init__(self, user, base):
        self.user = user
        self.epic = base
        self.controller_employee = EpicManagerEmployee(self.user, self.epic)
        self.controller_client = EpicManagerClient(self.user, self.epic)

    @is_authenticated
    @is_manager
    def update_event(self):
        try:
            supports = self.epic.dbemployees.get_supports()
            supports = [s.username for s in supports]
            support = EmployeeView.prompt_select_support(supports)
            contracts = self.epic.dbcontracts.get_active_contracts()
            contracts = [c.ref for c in contracts]
            contract = ContractView.prompt_select_contract(contracts)
            events = self.epic.dbevents.get_events(
                contract_ref=contract, state_code='U',
                support_name=EventView.no_support())
            events = [e.title for e in events]
            if events:
                event_title = EventView.prompt_select_event(events)
                self.epic.dbevents.update(contract, event_title, support)
                DataView.display_workflow()
                self.epic.dbemployees.create_task(
                    support,
                    EventView.workflow_affect(event_title)
                )
            else:
                EventView.no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_support
    def cancel_event(self):
        try:
            events = self.epic.dbevents.get_events(
                support_name=self.user.username, state_code='U')
            events = [f'{e.contract.ref}|{e.title}' for e in events]
            if events:
                try:
                    event = EventView.prompt_select_event(events)
                    self.epic.dbevents.cancel(event)
                except KeyboardInterrupt:
                    DataView.display_interupt()
            else:
                EventView.display_no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_support
    def terminate_event(self):
        try:
            events = self.epic.dbevents.get_events(
                support_name=self.user.username, state_code='U')
            events = [f'{e.contract.ref}|{e.title}' for e in events]
            if events:
                try:
                    event = EventView.prompt_select_event(events)
                    rapport = EventView.prompt_rapport()
                    self.epic.dbevents.terminate(event, rapport)
                    (contract_ref, none) = event.split('|')
                    # workflow
                    result = ContractView.prompt_confirm_close_contract()
                    if result:
                        managers = self.epic.dbemployees.get_managers()
                        manager = random.choice(managers)
                        DataView.display_workflow()
                        self.epic.dbemployees.create_task(
                            manager.username,
                            ContractView.workflow_contract_is_over(
                                contract_ref)
                        )
                except KeyboardInterrupt:
                    DataView.display_interupt()
            else:
                EventView.display_no_event()
        except KeyboardInterrupt:
            DataView.display_interupt()

    @sentry_activate
    @is_authenticated
    @is_commercial
    def create_event(self):
        contracts = self.epic.dbcontracts.get_contracts(
            commercial_name=self.user.username, state_value='S')
        if contracts:
            contracts = [c.ref for c in contracts]
            contract = ContractView.prompt_select_contract(contracts)
            types = self.epic.dbevents.get_types()
            types = [r.title for r in types]
            try:
                type = EventView.prompt_select_type(types)
                data = EventView.prompt_data_event()
                self.epic.dbevents.create(contract, type, data)
                # workflow creation
                DataView.display_workflow()
                managers = self.epic.dbemployees.get_managers()
                manager = random.choice(managers)
                self.epic.dbemployees.create_task(
                    manager.username,
                    EventView.workflow_ask_affect(data['title']))
            except KeyboardInterrupt:
                DataView.display_interupt()
        else:
            DataView.display_nocontracts()

    @sentry_activate
    @is_authenticated
    def list_of_events(self):
        contract_ref = None
        sname = None
        cname = self.controller_employee.choice_commercial()
        client = self.controller_client.choice_client(cname)
        # select a contract
        result = ContractView.prompt_confirm_contract()
        if result:
            contracts = self.epic.dbcontracts.get_contracts(
                cname, client)
            contracts_ref = [c.ref for c in contracts]
            contract_ref = ContractView.prompt_select_contract(contracts_ref)
        # select a support
        result = EmployeeView.prompt_confirm_support()
        if result:
            supports = self.epic.dbemployees.get_supports()
            supports_name = [c.username for c in supports]
            supports_name.append(EventView.no_support())
            sname = EmployeeView.prompt_select_support(supports_name)
        # display list
        events = self.epic.dbevents.get_events(
            cname, client, contract_ref, sname)
        EventView.display_list_events(events)
