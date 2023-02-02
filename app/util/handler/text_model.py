from collections.abc import Awaitable, Callable

from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram.types import User as TelegramUser
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.user import add_used_tokens_by_telegram_id
from app.state.customer import TextModelSG
from app.util.openai.text_model import TextModel


def create_text_model_handler(
    text_model: TextModel,
) -> Callable[[Message, MessageInput, DialogManager], Awaitable[None]]:
    async def text_model_handler(
        message: Message,
        _message_input: MessageInput,
        dialog_manager: DialogManager,
    ) -> None:
        if not message.text:
            await message.reply(text="Please provide a text prompt.")
            return

        text_model_prompt: Callable[[str, TextModel], tuple[str, int]]
        text_model_prompt = dialog_manager.middleware_data["text_model_prompt"]
        response_text, token_used = text_model_prompt(message.text, text_model)

        async_session: AsyncSession = dialog_manager.middleware_data["async_session"]
        telegram_user: TelegramUser = dialog_manager.middleware_data["telegram_user"]

        await add_used_tokens_by_telegram_id(
            async_session=async_session,
            telegram_id=telegram_user.id,
            tokens_used=token_used,
        )

        await message.reply(text=response_text)

    return text_model_handler


def get_text_model_state(text_model: TextModel) -> State:
    if text_model == "text-davinci-003":
        return TextModelSG.davinci

    if text_model == "text-curie-001":
        return TextModelSG.curie

    if text_model == "text-babbage-001":
        return TextModelSG.babbage

    if text_model == "text-ada-001":
        return TextModelSG.ada

    raise NotImplementedError(
        "Unknown text model: {text_model}".format(text_model=text_model),
    )
