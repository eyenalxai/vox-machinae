from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Const

from app.state.manager import MainManagerSG
from app.util.handler.allow_state import (
    back_to_select_allow_action,
    switch_to_allow_handler,
    switch_to_disallow_handler,
    user_allow_setter,
)


def build_admin_dialog() -> Dialog:
    return Dialog(
        Window(
            Row(
                Button(
                    Const("Allow user"),
                    id="allow",
                    on_click=switch_to_allow_handler,
                ),
                Button(
                    Const("Disallow user"),
                    id="disallow",
                    on_click=switch_to_disallow_handler,
                ),
            ),
            state=MainManagerSG.menu,
        ),
        Window(
            Const("Enter telegram ID of user to allow"),
            Button(
                Const("Back to menu"),
                id="back_to_menu",
                on_click=back_to_select_allow_action,
            ),
            MessageInput(user_allow_setter(future_allowed_state=True)),
            state=MainManagerSG.allow_user,
        ),
        Window(
            Const("Enter telegram ID of user to disallow"),
            Button(
                Const("Back to menu"),
                id="back_to_menu",
                on_click=back_to_select_allow_action,
            ),
            MessageInput(user_allow_setter(future_allowed_state=False)),
            state=MainManagerSG.disallow_user,
        ),
    )
