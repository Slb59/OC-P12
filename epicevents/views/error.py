from .console import error_console


def display_error_login():
    error_console.print('ERROR : Utilisateur ou mot de passe inconnu')


def display_token_expired():
    s = 'ERROR : Token expiré ! veuillez vous reconnecter.\n'
    s += 'commande: python epicevent.py --login username/password'
    error_console.print(s)


def display_token_invalid():
    error_console.print('ERROR : Token invalide! veuillez vous reconnecter.')


def display_not_commercial():
    error_console.print('ERROR : Accès refusé, rôle commercial requis.')


def display_not_manager():
    error_console.print('ERROR : Accès refusé, rôle manager requis.')


def display_not_support():
    error_console.print('ERROR : Accès refusé, rôle support requis.')
