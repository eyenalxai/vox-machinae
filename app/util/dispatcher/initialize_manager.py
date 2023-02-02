from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager, DialogRegistry, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from app.config.log import logger
from app.dialog.manager.access_menu import build_access_menu_dialog
from app.dialog.manager.main_menu import build_main_menu_dialog
from app.middleware.admin import filter_non_admin
from app.state.manager import MainManagerSG
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher


async def start_manager_dialog(
    _message: Message,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.start(MainManagerSG.main_menu, mode=StartMode.RESET_STACK)


async def error_handler(event: ErrorEvent, dialog_manager: DialogManager) -> None:
    if isinstance(event.exception, UnknownIntent):
        logger.error("Unknown intent: %s", event.exception)
        return await dialog_manager.start(
            MainManagerSG.main_menu,
            mode=StartMode.RESET_STACK,
        )

    if isinstance(event.exception, UnknownState):
        logger.error("Unknown state: %s", event.exception)
        await dialog_manager.reset_stack()
        return await dialog_manager.start(
            MainManagerSG.main_menu,
            mode=StartMode.RESET_STACK,
        )

    return UNHANDLED


def initialize_manager_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()

    registry = DialogRegistry(dispatcher)
    registry.register_start_handler(MainManagerSG.main_menu)

    main_dialog = build_main_menu_dialog()
    access_dialog = build_access_menu_dialog()

    registry.register(main_dialog)
    registry.register(access_dialog)

    dispatcher.message.register(start_manager_dialog, Command("manage"))
    dispatcher.errors.register(error_handler)

    dispatcher.message.middleware.register(filter_non_admin)  # type: ignore
    return dispatcher
