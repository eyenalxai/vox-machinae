from collections.abc import Callable

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.user import add_used_tokens_by_telegram_id
from app.util.model_from_state import text_model_from_state_value
from app.util.openai.text_model import TextModel

text_model_router = Router(name="text_model_router")


@text_model_router.message()
async def oof(  # noqa: WPS211 Found too many arguments: 6 > 5
    message: Message,
    message_text: str,
    async_session: AsyncSession,
    text_prompt: Callable[[str, TextModel], tuple[str, int]],
    telegram_user: TelegramUser,
    state: FSMContext,
) -> None:
    state_value = await state.get_state()
    text_model = text_model_from_state_value(state_value=state_value)

    response_text, token_used = text_prompt(message_text, text_model)

    await add_used_tokens_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_user.id,
        tokens_used=token_used,
    )

    await message.reply(text=response_text)
