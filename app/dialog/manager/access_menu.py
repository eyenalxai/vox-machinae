from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Start, SwitchTo
from aiogram_dialog.widgets.text import Const

from app.state.manager import AccessManagerSG, MainManagerSG
from app.util.handler.allow_state import user_allow_setter


def build_access_menu_dialog() -> Dialog:
    switch_to_access_menu = SwitchTo(
        Const("Back to access menu"),
        id="back_to_menu",
        state=AccessManagerSG.access_menu,
    )
    return Dialog(
        Window(
            Const("Select Action"),
            Row(
                SwitchTo(
                    Const("Allow User"),
                    id="allow",
                    state=AccessManagerSG.allow_user,
                ),
                SwitchTo(
                    Const("Disallow User"),
                    id="disallow",
                    state=AccessManagerSG.disallow_user,
                ),
            ),
            Start(
                Const("Back to Main Menu"),
                id="back_to_main_menu",
                state=MainManagerSG.main_menu,
            ),
            state=AccessManagerSG.access_menu,
        ),
        Window(
            Const("Enter Telegram ID of a User to Allow"),
            switch_to_access_menu,
            MessageInput(user_allow_setter(future_allowed_state=True)),
            state=AccessManagerSG.allow_user,
        ),
        Window(
            Const("Enter Telegram ID of a User to Disallow"),
            switch_to_access_menu,
            MessageInput(user_allow_setter(future_allowed_state=False)),
            state=AccessManagerSG.disallow_user,
        ),
    )
