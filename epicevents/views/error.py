from rich import print as rprint


def display_error_login():
    rprint('[bold red]ERROR : Utilisateur ou mot de passe inconnu')


def display_token_expired():
    rprint('[bold red]ERROR : Token expiré ! veuillez vous reconnecter.')


def display_token_invalid():
    rprint('[bold red]ERROR : Token invalide! veuillez vous reconnecter.')
