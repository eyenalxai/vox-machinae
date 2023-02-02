from collections.abc import Awaitable, Callable

from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State
from aiogram.types.error_event import ErrorEvent
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from app.config.log import logger


def get_error_handler(  # noqa: WPS212, WPS217
    reset_state: State,
) -> Callable[[ErrorEvent, DialogManager], Awaitable[None]]:
    async def error_handler(  # noqa: WPS217
        event: ErrorEvent,
        dialog_manager: DialogManager,
    ) -> None:
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

        if isinstance(event.exception, TelegramBadRequest):
            logger.error("TelegramBadRequest: %s", event.exception)
            if not event.update.message:
                logger.error("No message in update? %s", event.update)
                await dialog_manager.reset_stack()
                return await dialog_manager.start(
                    reset_state,
                    mode=StartMode.RESET_STACK,
                )

            await event.update.message.reply(
                "\n\n".join(
                    [
                        "Received answer from OpenAI which Telegram couldn't handle",
                        "Try asking in a different way",
                    ],
                ),
            )
            return None

        return UNHANDLED

    return error_handler
