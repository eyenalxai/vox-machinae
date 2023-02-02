from collections.abc import Callable

from aiogram.types import Message, URLInputFile
from aiogram.types import User as TelegramUser
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.user import add_used_tokens_by_telegram_id
from app.util.other import random_string


async def image_from_text_model_handler(
    message: Message,
    _message_input: MessageInput,
    dialog_manager: DialogManager,
) -> None:
    if not message.text:
        await message.reply(text="Please provide a text prompt.")
        return

    image_from_text_model_prompt: Callable[[str], tuple[str, int]]
    image_from_text_model_prompt = dialog_manager.middleware_data[
        "image_from_text_model_prompt"
    ]
    try:
        response_text, tokens_used = image_from_text_model_prompt(message.text)
    except HTTPStatusError:
        await message.reply(text="There was an error with the OpenAI API")
        return

    async_session: AsyncSession = dialog_manager.middleware_data["async_session"]
    telegram_user: TelegramUser = dialog_manager.middleware_data["telegram_user"]

    await add_used_tokens_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_user.id,
        tokens_used=tokens_used,
    )

    await message.reply_photo(
        photo=URLInputFile(
            url=response_text,
            filename="{filename}.png".format(filename=random_string()),
        ),
        caption="Here is your image.",
    )
