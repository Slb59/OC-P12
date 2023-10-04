from epicevents.views.contract_views import ContractView
from .utils import (
    KeyInputs, ask_with_patched_input,
    ask_with_patched_select)


def test_prompt_confirm_contract():
    text = "y" + KeyInputs.ENTER + "\r"
    result = ask_with_patched_input(
        ContractView.prompt_confirm_contract, text)
    assert result


def test_prompt_contract():
    text = KeyInputs.DOWN + KeyInputs.ENTER + KeyInputs.ENTER + "\r"
    choice = ['ref1', 'ref2', 'ref3']
    result = ask_with_patched_select(
        ContractView.prompt_contract, text, choice)
    assert result == "ref2"


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
