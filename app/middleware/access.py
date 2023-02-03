from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message, TelegramObject
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import logger
from app.query.user import is_allowed_by_telegram_id


async def filter_non_allowed(
    handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
    message: TelegramObject,
    data: dict[str, Any],
) -> Any:
    if not isinstance(message, Message):
        raise TypeError("message is not a Message")

    async_session: AsyncSession = data["async_session"]
    telegram_user: TelegramUser = data["telegram_user"]

    is_allowed = await is_allowed_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_user.id,
    )

    if not is_allowed:
        await message.answer("You are not allowed to use this bot")
        logger.warning(
            "User {full_name} is not allowed to use this bot".format(
                full_name=telegram_user.full_name,
            ),
        )
        return None

    return await handler(message, data)
