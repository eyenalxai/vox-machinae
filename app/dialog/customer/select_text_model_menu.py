from collections.abc import Awaitable, Callable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const

from app.state.customer import MainCustomerSG, SelectTextModelSG, TextModelSG
from app.util.model_from_state import text_model_from_state_value
from app.util.other import pretty_text_model_name


def select_function(
    text_model_state: State,
) -> Callable[[CallbackQuery, Button, DialogManager], Awaitable[None]]:
    async def select_model(
        callback: CallbackQuery,
        _button: Button,
        dialog_manager: DialogManager,
    ) -> None:
        state: FSMContext = dialog_manager.middleware_data.get("state")  # type: ignore
        await state.set_state(text_model_state)

        state_value = await state.get_state()
        text_model = text_model_from_state_value(state_value=state_value)
        await callback.answer(
            text="Selected model: {pretty_name}".format(
                pretty_name=pretty_text_model_name(text_model=text_model),
            ),
        )

    return select_model


def build_select_text_model_menu_dialog() -> Dialog:
    return Dialog(
        Window(
            Const("Select Text Model"),
            Row(
                Button(
                    Const("Davinci"),
                    id="davinci",
                    on_click=select_function(text_model_state=TextModelSG.davinci),
                ),
                Button(
                    Const("Curie"),
                    id="curie",
                    on_click=select_function(text_model_state=TextModelSG.curie),
                ),
                Button(
                    Const("Babbage"),
                    id="babbage",
                    on_click=select_function(text_model_state=TextModelSG.babbage),
                ),
                Button(
                    Const("Ada"),
                    id="ada",
                    on_click=select_function(text_model_state=TextModelSG.ada),
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
