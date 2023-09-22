import questionary


def prompt_confirm_commercial():
    return questionary.confirm(
        "Souhaitez-vous sélectionner un commercial ?").ask()


def prompt_commercial(all_commercials):
    return questionary.select(
        "Choix du commercial:",
        choices=all_commercials,
    ).ask()
