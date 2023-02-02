from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from app.state.customer import ImageFromTextSG, MainCustomerSG
from app.util.handler.image_from_text_model import image_from_text_model_handler


def build_image_from_text_model_prompt_dialog() -> Dialog:
    return Dialog(
        Window(
            Const("Enter prompt for Image Generation:"),
            MessageInput(image_from_text_model_handler),
            Start(
                Const("Back to Main Menu"),
                id="back_to_customer_main_menu",
                state=MainCustomerSG.main_menu,
            ),
            state=ImageFromTextSG.image_model,
        ),
    )
