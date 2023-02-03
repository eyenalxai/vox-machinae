from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogRegistry, StartMode

from app.dialog.customer.image_from_text_model_prompt import (
    build_image_from_text_model_prompt_dialog,
)
from app.dialog.customer.main_menu import build_customer_main_menu_dialog
from app.dialog.customer.select_text_model_menu import (
    build_select_text_model_menu_dialog,
)
from app.dialog.customer.text_model_prompt import build_text_model_prompt_dialog
from app.middleware.access import filter_non_allowed
from app.middleware.user import update_user
from app.state.customer import MainCustomerSG
from app.util.dispatcher.error_handler import get_error_handler
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher
from app.util.openai.image_from_text_model import openai_image_from_text_model_wrapper
from app.util.openai.text_model import openai_text_model_wrapper
from app.util.settings.customer import customer_settings


async def start_customer_dialog(
    _message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MainCustomerSG.main_menu, mode=StartMode.RESET_STACK)


def register_customer_dialogs(dispatcher: Dispatcher) -> DialogRegistry:
    main_customer_dialog = build_customer_main_menu_dialog()
    select_text_model_menu_dialog = build_select_text_model_menu_dialog()
    text_model_prompt_dialog = build_text_model_prompt_dialog()
    image_from_text_model_prompt_dialog = build_image_from_text_model_prompt_dialog()

    registry = DialogRegistry(dp=dispatcher)
    registry.register(dialog=main_customer_dialog)
    registry.register(dialog=select_text_model_menu_dialog)
    registry.register(dialog=text_model_prompt_dialog)
    registry.register(dialog=image_from_text_model_prompt_dialog)

    return registry


def initialize_customer_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()
    dispatcher["text_model_prompt"] = openai_text_model_wrapper()
    dispatcher["image_from_text_model_prompt"] = openai_image_from_text_model_wrapper()

    dispatcher.message.register(
        start_customer_dialog,
        Command(customer_settings.settings_command),
    )

    register_customer_dialogs(dispatcher=dispatcher)

    error_handler = get_error_handler(reset_state=MainCustomerSG.main_menu)
    dispatcher.errors.register(error_handler)

    dispatcher.message.middleware(update_user)
    dispatcher.message.middleware(filter_non_allowed)

    return dispatcher
