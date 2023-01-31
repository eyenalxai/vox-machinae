from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.user import allow_user_by_telegram_id

admin_router = Router(name="start router")


@admin_router.message(Command("allow"))
async def command_allow_handler(
    message: Message,
    async_session: AsyncSession,
) -> None:
    if not message.text:
        await message.reply(text="Usage: /allow <i>telegram_user_id</i>")
        return

    words = message.text.split()

    if len(words) != 2:
        await message.reply(text="Usage: /allow <i>telegram_user_id</i>")
        return

    _, user_id = words

    try:
        int_user_id = int(user_id)
    except ValueError:
        await message.reply(text="Invalid user id provided")
        return

    user = await allow_user_by_telegram_id(
        async_session=async_session,
        telegram_id=int_user_id,
    )

    await message.reply(
        text="Allowed user with id: {telegram_id}".format(telegram_id=user.telegram_id),
    )
