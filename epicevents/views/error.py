from .console import error_console


class ErrorView:

    @classmethod
    def display_error_login(cls):
        error_console.print('ERROR : Utilisateur ou mot de passe inconnu')

    @classmethod
    def display_token_expired(cls):
        s = 'ERROR : Token expiré ! veuillez vous reconnecter.\n'
        s += 'commande: python epicevent.py login'
        error_console.print(s)

    @classmethod
    def display_token_invalid(cls):
        error_console.print(
            'ERROR : Token invalide! veuillez vous reconnecter.')

    @classmethod
    def display_not_commercial(cls):
        error_console.print('ERROR : Accès refusé, rôle commercial requis.')

    @classmethod
    def display_not_manager(cls):
        error_console.print('ERROR : Accès refusé, rôle manager requis.')

    @classmethod
    def display_not_support(cls):
        error_console.print('ERROR : Accès refusé, rôle support requis.')

    @classmethod
    def dsiplay_error_exception(cls, text):
        error_console.print('Une erreur est survenu dans le traitement')
        error_console.print(text)
