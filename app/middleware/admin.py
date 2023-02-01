from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message
from aiogram.types import User as TelegramUser

from app.util.settings.manager import manager_settings


async def filter_non_admin(
    handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: dict[str, Any],
) -> Any:
    telegram_user: TelegramUser = data["telegram_user"]

    if telegram_user.id not in manager_settings.admin_user_ids:
        return await message.answer(
            "You are not allowed to manage this bot",
        )

    return await handler(message, data)
