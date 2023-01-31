from collections.abc import Callable

from aiogram import Router
from aiogram.types import Message

text_router = Router(name="text router")


@text_router.message()
async def command_start_handler(
    message: Message,
    message_text: str,
    text_prompt: Callable[[str], str],
) -> None:
    response_text = text_prompt(message_text)

    await message.reply(text=response_text)
