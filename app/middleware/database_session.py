from collections.abc import Awaitable, Callable
from typing import Any

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.log import logger


async def get_async_database_session(
    handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
    message: Message,
    data: dict[str, Any],
) -> Any:
    try:
        async with AsyncSession(bind=data["async_engine"]) as async_session:
            async with async_session.begin():
                data["async_session"] = async_session
                return await handler(message, data)
    except Exception as exception:
        logger.error("Error: %s", exception)  # noqa: G200
        await message.reply("An error occurred. Please try again.")
        return None
