from rich import print as rprint


def display_error_login():
    rprint('[bold red]ERROR : Utilisateur ou mot de passe inconnu')


def display_token_expired():
    s = '[bold red]ERROR : Token expiré ! veuillez vous reconnecter.\n'
    s += 'commande: python epicevent.py --login username/password'
    rprint(s)


def display_token_invalid():
    rprint('[bold red]ERROR : Token invalide! veuillez vous reconnecter.')


def display_not_commercial():
    rprint('[bold red]ERROR : Accès refusé, rôle commercial requis.')


def display_not_manager():
    rprint('[bold red]ERROR : Accès refusé, rôle manager requis.')


def display_not_support():
    rprint('[bold red]ERROR : Accès refusé, rôle support requis.')
