from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from app.state.customer import SelectTextModelSG
from app.util.handler.text_model import create_text_model_handler, get_text_model_state
from app.util.openai.text_model import TextModel
from app.util.other import pretty_text_model_name


def build_text_model_prompt_dialog() -> Dialog:
    def text_model_prompt(text_model: TextModel) -> Window:
        pretty_name = pretty_text_model_name(text_model=text_model)
        state = get_text_model_state(text_model=text_model)
        return Window(
            Const("Enter prompt for {pretty_name}:".format(pretty_name=pretty_name)),
            MessageInput(create_text_model_handler(text_model=text_model)),
            Start(
                Const("Back to Text Model Selection"),
                id="back_to_model_selection",
                state=SelectTextModelSG.select_text_model_menu,
            ),
            state=state,
        )

    return Dialog(
        text_model_prompt(text_model="text-davinci-003"),
        text_model_prompt(text_model="text-curie-001"),
        text_model_prompt(text_model="text-babbage-001"),
        text_model_prompt(text_model="text-ada-001"),
    )
