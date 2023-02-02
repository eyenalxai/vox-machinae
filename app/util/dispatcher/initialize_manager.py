from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogRegistry, StartMode

from app.dialog.manager.access_menu import build_access_menu_dialog
from app.dialog.manager.main_menu import build_manager_main_menu_dialog
from app.middleware.admin import filter_non_admin
from app.state.manager import MainManagerSG
from app.util.dispatcher.error_handler import get_error_handler
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher
from app.util.settings.manager import manager_settings


async def start_manager_dialog(
    _message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MainManagerSG.main_menu, mode=StartMode.RESET_STACK)


def initialize_manager_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()
    registry = DialogRegistry(dispatcher)

    main_manager_dialog = build_manager_main_menu_dialog()
    access_dialog = build_access_menu_dialog()

    registry.register(main_manager_dialog)
    registry.register(access_dialog)

    dispatcher.message.register(
        start_manager_dialog,
        Command(manager_settings.manager_command),
    )

    error_handler = get_error_handler(reset_state=MainManagerSG.main_menu)
    dispatcher.errors.register(error_handler)

    dispatcher.message.middleware.register(filter_non_admin)  # type: ignore
    return dispatcher
