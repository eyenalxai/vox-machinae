from collections.abc import Awaitable, Callable

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy.ext.asyncio import AsyncSession

from app.query.user import set_allowed_user_by_telegram_id
from app.state.manager import MainManagerSG


def user_allow_setter(
    future_allowed_state: bool,
) -> Callable[[Message, MessageInput, DialogManager], Awaitable[None]]:
    async def allow_state_handler(
        message: Message,
        _message_input: MessageInput,
        manager: DialogManager,
    ) -> None:
        if not message.text:
            await message.reply(text="Please provide a user id.")
            return

        user_id = message.text

        try:
            int_user_id = int(user_id)
        except ValueError:
            await message.reply(text="Invalid user id provided")
            return

        async_session: AsyncSession = manager.middleware_data["async_session"]

        user = await set_allowed_user_by_telegram_id(
            async_session=async_session,
            telegram_id=int_user_id,
            is_allowed=future_allowed_state,
        )

        allowed_state = "Allowed" if future_allowed_state else "Disallowed"

        await message.reply(
            text="{allowed_state} user with id: {telegram_id}".format(
                telegram_id=user.telegram_id,
                allowed_state=allowed_state,
            ),
        )

    return allow_state_handler


async def switch_to_allow_handler(
    _callback: CallbackQuery,
    _button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(MainManagerSG.allow_user)


async def switch_to_disallow_handler(
    _callback: CallbackQuery,
    _button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(MainManagerSG.disallow_user)


async def back_to_select_allow_action(
    _callback: CallbackQuery,
    _button: Button,
    manager: DialogManager,
) -> None:
    await manager.switch_to(MainManagerSG.menu)
