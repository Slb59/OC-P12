from epicevents.controllers.config import Config


class MockFunction:
    @classmethod
    def mock_base(cls, *args, **kwargs):
        return Config('tests/functionnal/database_userstories.ini')

    @classmethod
    def mock_prompt_login(cls):
        return ("Osynia", "osyA!111")

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
