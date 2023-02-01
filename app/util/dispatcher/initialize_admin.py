from aiogram import Dispatcher
from aiogram import F as MagicFilter
from aiogram.types import Message
from aiogram_dialog import DialogManager, DialogRegistry, StartMode

from app.dialog.admin import build_admin_dialog
from app.state.manager import MainManagerSG
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher


async def start_admin_dialog(_message: Message, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainManagerSG.menu, mode=StartMode.RESET_STACK)


def initialize_admin_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()

    registry = DialogRegistry(dispatcher)
    registry.register_start_handler(MainManagerSG.menu)

    admin_dialog = build_admin_dialog()
    registry.register(admin_dialog)

    dispatcher.message.register(start_admin_dialog, MagicFilter.text == "/start")
    return dispatcher
