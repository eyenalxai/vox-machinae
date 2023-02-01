from aiogram import Dispatcher
from aiogram import F as MagicFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogRegistry, StartMode

from app.dialog.manager import build_manager_dialog
from app.middleware.admin import filter_non_admin
from app.state.manager import MainManagerSG
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher


async def start_manager_dialog(
    _message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MainManagerSG.menu, mode=StartMode.RESET_STACK)


def initialize_manager_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()

    registry = DialogRegistry(dispatcher)
    registry.register_start_handler(MainManagerSG.menu)

    manager_dialog = build_manager_dialog()
    registry.register(manager_dialog)

    dispatcher.message.register(start_manager_dialog, MagicFilter.text == "/start")

    dispatcher.message.middleware.register(filter_non_admin)  # type: ignore
    return dispatcher
