from epicevents.views.error import (
    display_error_login,
    display_token_expired
)

from epicevents.views.console import error_console


def test_display_error_login():
    with error_console.capture() as capture:
        display_error_login()
    str_output = capture.get()
    assert str_output == 'ERROR : Utilisateur ou mot de passe inconnu\n'


def test_display_token_expired():
    with error_console.capture() as capture:
        display_token_expired()
    str_output = capture.get()
    s = 'ERROR : Token expiré ! veuillez vous reconnecter.\n'
    s += 'commande: python epicevent.py --login username/password\n'
    assert str_output == s
