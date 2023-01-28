from collections.abc import Callable

from aiogram import Router
from aiogram.types import Message

main_router = Router(name="main router")


@main_router.message()
async def message_handler(
    message: Message,
    message_text: str,
    create_prompt: Callable[[str], str],
) -> None:
    response_text = create_prompt(message_text)

    await message.reply(text=response_text)
