import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message

from app.settings import settings


async def filter_not_allowed_user(
    handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: dict[str, Any],
) -> Any:
    if not message.from_user:
        logging.error("No user in message?! Message: %s", message)
        return None

    if message.from_user.id not in settings.allowed_user_ids:
        logging.error(
            "User %s - @%s is not allowed to use this bot!",
            message.from_user.full_name,
            message.from_user.username or "None",
        )
        return None

    return await handler(message, data)
