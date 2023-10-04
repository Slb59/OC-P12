from epicevents.views.error import ErrorView

from epicevents.views.console import error_console


def test_display_error_login():
    with error_console.capture() as capture:
        ErrorView.display_error_login()
    str_output = capture.get()
    assert str_output == 'ERROR : Utilisateur ou mot de passe inconnu\n'


def test_display_token_expired():
    with error_console.capture() as capture:
        ErrorView.display_token_expired()
    str_output = capture.get()
    s = 'ERROR : Token expiré ! veuillez vous reconnecter.\n'
    s += 'commande: python epicevent.py login\n'
    assert str_output == s


def test_display_token_invalid():
    with error_console.capture() as capture:
        ErrorView.display_token_invalid()
    str_output = capture.get()
    s = "ERROR : Token invalide! veuillez vous reconnecter.\n"
    assert str_output == s


def test_display_not_commercial():
    with error_console.capture() as capture:
        ErrorView.display_not_commercial()
    str_output = capture.get()
    s = "ERROR : Accès refusé, rôle commercial requis.\n"
    assert str_output == s


def test_display_not_manager():
    with error_console.capture() as capture:
        ErrorView.display_not_manager()
    str_output = capture.get()
    s = "ERROR : Accès refusé, rôle manager requis.\n"
    assert str_output == s


def test_display_not_support():
    with error_console.capture() as capture:
        ErrorView.display_not_support()
    str_output = capture.get()
    s = "ERROR : Accès refusé, rôle support requis.\n"
    assert str_output == s
