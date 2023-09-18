def display_logout() -> None:
    text = "Vous êtes déconnecté"
    print(text)


def display_welcome(username) -> None:
    text = f" Bienvenue {username} sur EpicEvent"
    print(len(text) * '-')
    print(text)
    print(len(text) * '-')
    print('')
