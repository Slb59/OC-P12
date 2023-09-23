from rich.panel import Panel
from rich import box
from rich.align import Align
from epicevents.views.console import console


class DataView:

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
