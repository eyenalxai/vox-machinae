from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from app.state.customer import MainCustomerSG, SelectTextModelSG, TextModelSG


def build_select_text_model_menu_dialog() -> Dialog:
    return Dialog(
        Window(
            Const("Use Text Model"),
            Row(
                Start(
                    Const("Davinci"),
                    id="davinci",
                    state=TextModelSG.davinci,
                ),
                Start(
                    Const("Curie"),
                    id="curie",
                    state=TextModelSG.curie,
                ),
                Start(
                    Const("Babbage"),
                    id="babbage",
                    state=TextModelSG.babbage,
                ),
                Start(
                    Const("Ada"),
                    id="ada",
                    state=TextModelSG.ada,
                ),
            ),
            Start(
                Const("Back to Main Menu"),
                id="back_to_customer_main_menu",
                state=MainCustomerSG.main_menu,
            ),
            state=SelectTextModelSG.select_text_model_menu,
        ),
    )
