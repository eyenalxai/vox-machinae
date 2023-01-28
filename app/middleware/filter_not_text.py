import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message


async def filter_not_text(
    handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: dict[str, Any],  # noqa: WPS110 Found wrong variable name: data
) -> Any:
    if not message.from_user:
        return None

    if not message.text:
        logging.error(
            "No text in message?! User: %s - @%s",
            message.from_user.full_name,
            message.from_user.username,
        )
        return None

    data["message_text"] = message.text

    return await handler(message, data)
