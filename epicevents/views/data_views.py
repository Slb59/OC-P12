from rich.panel import Panel
from rich import box
from rich.align import Align
from epicevents.views.console import console


class DataView:

    @classmethod
    def display_nocontracts(cls):
        console.print('Aucun contrat trouvé')

    @classmethod
    def display_interupt(cls):
        console.print('Opération abandonée')

    @classmethod
    def display_error_contract_amount(cls):
        console.print('Ce montant est supérieur au restant dû')

    @classmethod
    def display_commercial_with_contracts(cls):
        console.print('Ce commercial gère des contracts actifs')

    @classmethod
    def display_need_one_manager(cls):
        console.print('La base doit contenir au moins un manager')

    @classmethod
    def display_error_unique(cls):
        console.print('Impossible: cet enregistrement existe déjà')

    @classmethod
    def display_error_contract_need_c(cls):
        console.print("Le contract doit être à l'état créé")

    @classmethod
    def display_data_update(cls):
        console.print('Vos modifications ont été enregistrées')

    @classmethod
    def display_profil(cls, e, nb):
        text = f'Email: {e.email}\n' if e.email else 'Email: \n'
        text += f'Role: {e.role.value}\n'
        text += f'Etat: {e.state.value}\n'
        text += f'Département: {e.department.name}\n'
        text += f'Nb de tâches en cours: {str(nb)}\n'
        p = Panel(
            Align.center(text, vertical='bottom'),
            box=box.ROUNDED,
            title_align='center',
            title=e.username)
        console.print(p)
