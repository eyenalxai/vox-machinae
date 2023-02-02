from collections.abc import Awaitable, Callable

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.fsm.state import State
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from app.config.log import logger


def get_error_handler(
    reset_state: State,
) -> Callable[[ErrorEvent, DialogManager], Awaitable[None]]:
    async def error_handler(event: ErrorEvent, dialog_manager: DialogManager) -> None:
        if isinstance(event.exception, UnknownIntent):
            logger.error("Unknown intent: %s", event.exception)
            return await dialog_manager.start(
                reset_state,
                mode=StartMode.RESET_STACK,
            )

        if isinstance(event.exception, UnknownState):
            logger.error("Unknown state: %s", event.exception)
            await dialog_manager.reset_stack()
            return await dialog_manager.start(
                reset_state,
                mode=StartMode.RESET_STACK,
            )

        return UNHANDLED

    return error_handler
