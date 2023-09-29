import questionary


class PromptView:

    @classmethod
    def prompt_confirm_statut(cls, **kwargs):
        return questionary.confirm(
            "Souhaitez-vous sélectionner un statut ?", **kwargs).ask()

    @classmethod
    def prompt_statut(cls, all_states):
        return questionary.select(
            "Choix du statut:",
            choices=all_states,
        ).ask()
