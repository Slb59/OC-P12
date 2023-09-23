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

    @classmethod
    def prompt_confirm_statut(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un statut ?").ask()

    @classmethod
    def prompt_statut(cls, all_states):
        return questionary.select(
            "Choix du statut:",
            choices=all_states,
        ).ask()

    @classmethod
    def prompt_confirm_contract(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un contrat ?").ask()

    @classmethod
    def prompt_contract(cls, all_contracts):
        return questionary.select(
            "Choix du contrat:",
            choices=all_contracts,
        ).ask()

    @classmethod
    def prompt_confirm_support(cls):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un support ?").ask()

    @classmethod
    def prompt_support(cls, all_supports):
        return questionary.select(
            "Choix du support:",
            choices=all_supports,
        ).ask()

    @classmethod
    def prompt_confirm_task(cls):
        return questionary.confirm(
            "Souhaitez-vous finaliser une tache ?").ask()

    @classmethod
    def prompt_task(cls, all_tasks):
        return questionary.select(
            "Identifiant de la tâche à terminer:",
            choices=all_tasks,
        ).ask()
