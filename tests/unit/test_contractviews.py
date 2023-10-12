from epicevents.contract.contract_views import ContractView
from ..utils import (
    KeyInputs, ask_with_patched_input)


def test_prompt_confirm_contract():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        ContractView.prompt_confirm_contract, text)
    assert result


def test_prompt_data_contract():
    values = {
        'ref': 'ref1',
        'description': 'description',
        'total_amount': '10000'}

    text = values['ref'] + KeyInputs.ENTER\
        + values['description'] + KeyInputs.ENTER\
        + values['total_amount'] + KeyInputs.ENTER\
        + "\r"
    result = ask_with_patched_input(
        ContractView.prompt_data_contract, text)
    assert result == values


def test_prompt_data_paiement():
    values = {'ref': 'ref', 'amount': '1000'}
    text = values['ref'] + KeyInputs.ENTER\
        + values['amount'] + KeyInputs.ENTER\
        + "\r"
    result = ask_with_patched_input(
        ContractView.prompt_data_paiement, text)
    assert result == values


def test_confirm_close_contract():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        ContractView.prompt_confirm_close_contract, text)
    assert result


def test_workflow_contract_is_over():
    expected = "Evénements terminés, solder le contrat contract_ref"
    assert ContractView.workflow_contract_is_over("contract_ref") == expected
 