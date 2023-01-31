from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

start_router = Router(name="start router")


@start_router.message(Command("start", "help"))
async def command_start_handler(
    message: Message,
) -> None:
    await message.answer(text="Ask me anything")
