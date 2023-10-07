from epicevents.controllers.config import Config


class MockFunction:
    @classmethod
    def mock_base(cls, *args, **kwargs):
        return Config('tests/functionnal/database_userstories.ini')

    @classmethod
    def mock_login_osynia(cls):
        return ("Osynia", "osyA!111")

    @classmethod
    def mock_login_yuka(cls):
        return ("Yuka", "yukA!111")

    @classmethod
    def mock_login_aritomo(cls):
        return ("Aritomo", "ariT!111")

    @classmethod
    def mock_prompt_confirm_no(cls):
        return False

    @classmethod
    def mock_prompt_confirm_yes(cls):
        return True

    @classmethod
    def mock_prompt_commercial(cls, *args, **kwargs):
        return 'Yuka'

    @classmethod
    def mock_prompt_data_employee(cls, *args, **kwargs):
        return {
            'username': 'NewUser', 'password': 'newU!111',
            'email': 'nuser@epic.co', 'role': 'Commercial'}

    @classmethod
    def mock_prompt_baseinit(cls, *args, **kwargs):
        return ('epicStories', 'postgres', 'postG!111', '5432')

    @classmethod
    def mock_prompt_manager(cls, *args, **kwargs):
        return ('Osynia', 'osyA!111')

    @classmethod
    def mock_role_manager(cls, *args, **kwargs):
        return 'Manager'

    @classmethod
    def mock_role_commercial(cls, *args, **kwargs):
        return 'Commercial'

    @classmethod
    def mock_aritomo(cls, *args, **kwargs):
        return "Aritomo"

    @classmethod
    def mock_yuka(cls, *args, **kwargs):
        return "Yuka"

    @classmethod
    def mock_morihei(cls, *args, **kwargs):
        return "Morihei"

    @classmethod
    def mock_osynia(cls, *args, **kwargs):
        return "Osynia"

    @classmethod
    def mock_client0(cls, *args, **kwargs):
        return "Client n°0"

    @classmethod
    def mock_prompt_data_contract(cls, *args, **kwargs):
        return {'ref': 'contrat0', 'description': 'contrat0',
                'total_amount': '10000'}

    @classmethod
    def mock_contract0(cls, *args, **kwargs):
        return 'contrat0'

    @classmethod
    def mock_contract1(cls, *args, **kwargs):
        return 'contrat1'

    @classmethod
    def mock_choice1(cls, *args, **kwargs):
        return 1

    @classmethod
    def mock_choice3(cls, *args, **kwargs):
        return 3

    @classmethod
    def mock_event_contract1(cls, *args, **kwargs):
        return 'contrat1 event'

    @classmethod
    def mock_data_paiement_1000(cls, *args, **kwargs):
        return {'ref': 'paiement', 'amount': '1000'}

    @classmethod
    def mock_data_paiement_3000(cls, *args, **kwargs):
        return {'ref': 'paiement', 'amount': '3000'}

    @classmethod
    def mock_data_paiement_4000(cls, *args, **kwargs):
        return {'ref': 'paiement', 'amount': '4000'}
