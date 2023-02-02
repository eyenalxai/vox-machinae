from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogRegistry, StartMode

from app.dialog.customer.main_menu import build_customer_main_menu_dialog
from app.dialog.customer.select_text_model_menu import (
    build_select_text_model_menu_dialog,
)
from app.middleware.access import filter_non_allowed
from app.middleware.text import filter_not_text
from app.middleware.user import update_user
from app.route.customer.text_model import text_model_router
from app.state.customer import MainCustomerSG, TextModelSG
from app.util.dispatcher.error_handler import get_error_handler
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher
from app.util.openai.text_model import openai_text_wrapper
from app.util.settings.customer import customer_settings


async def start_customer_dialog(
    _message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MainCustomerSG.main_menu, mode=StartMode.RESET_STACK)


def initialize_customer_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()
    dispatcher["text_prompt"] = openai_text_wrapper()

    dispatcher.include_router(text_model_router)

    text_model_router.message.register(~Command(customer_settings.options_command))
    text_model_router.message.register(
        TextModelSG.davinci,
        TextModelSG.curie,
        TextModelSG.babbage,
        TextModelSG.ada,
    )
    text_model_router.message.middleware(filter_not_text)  # type: ignore

    main_customer_dialog = build_customer_main_menu_dialog()
    select_text_model_menu_dialog = build_select_text_model_menu_dialog()

    registry = DialogRegistry(dispatcher)
    registry.register(main_customer_dialog)
    registry.register(select_text_model_menu_dialog)

    dispatcher.message.register(
        start_customer_dialog,
        Command(customer_settings.options_command),
    )

    error_handler = get_error_handler(reset_state=MainCustomerSG.main_menu)
    dispatcher.errors.register(error_handler)

    dispatcher.message.middleware(update_user)  # type: ignore
    dispatcher.message.middleware(filter_non_allowed)  # type: ignore

    return dispatcher
