from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import logger
from app.query.user import save_or_update_user


async def filter_non_user(
    handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: dict[str, Any],
) -> Any:
    if not message.from_user:
        logger.error("No user in message?! Message: %s", message)
        return None

    data["telegram_user"] = message.from_user

    return await handler(message, data)


async def update_user(
    handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: dict[str, Any],
) -> Any:
    async_session: AsyncSession = data["async_session"]
    telegram_user: TelegramUser = data["telegram_user"]

    await save_or_update_user(
        async_session=async_session,
        telegram_user=telegram_user,
    )

    return await handler(message, data)
