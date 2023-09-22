import questionary


class PromptView:

    @classmethod
    def prompt_confirm_commercial(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un commercial ?").ask()

    @classmethod
    def prompt_commercial(cls, all_commercials):
        return questionary.select(
            "Choix du commercial:",
            choices=all_commercials,
        ).ask()

    @classmethod
    def prompt_confirm_client(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un client ?").ask()

    @classmethod
    def prompt_client(cls, all_clients):
        return questionary.select(
            "Choix du client:",
            choices=all_clients,
        ).ask()
