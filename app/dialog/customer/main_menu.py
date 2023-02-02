from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from app.state.customer import MainCustomerSG, SelectTextModelSG


def build_customer_main_menu_dialog() -> Dialog:
    return Dialog(
        Window(
            Const("Select Action"),
            Start(
                Const("Select Text Model"),
                id="select_text_model",
                state=SelectTextModelSG.select_text_model_menu,
            ),
            state=MainCustomerSG.main_menu,
        ),
    )
