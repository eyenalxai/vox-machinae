from collections.abc import Callable

from aiogram import Router
from aiogram.types import Message
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.user import add_used_tokens_by_telegram_id

text_router = Router(name="text router")


@text_router.message()
async def command_start_handler(
    message: Message,
    message_text: str,
    async_session: AsyncSession,
    text_prompt: Callable[[str], tuple[str, int]],
    telegram_user: TelegramUser,
) -> None:
    response_text, token_used = text_prompt(message_text)

    await add_used_tokens_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_user.id,
        tokens_used=token_used,
    )

    await message.reply(text=response_text)
