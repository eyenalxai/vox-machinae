from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from app.state.manager import AccessManagerSG, MainManagerSG


def build_main_menu_dialog() -> Dialog:
    return Dialog(
        Window(
            Const("Select Action"),
            Start(
                Const("Access Menu"),
                id="access",
                state=AccessManagerSG.access_menu,
            ),
            state=MainManagerSG.main_menu,
        ),
    )
