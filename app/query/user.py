from aiogram.types import User as TelegramUser
from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.models import UserModel


async def get_user_by_telegram_id(
    async_session: AsyncSession,
    telegram_id: int,
) -> UserModel | None:
    query = select(UserModel).where(UserModel.telegram_id == telegram_id)
    query_result = await async_session.execute(query)

    return query_result.scalars().first()


async def save_or_update_user(
    async_session: AsyncSession,
    telegram_user: TelegramUser,
) -> UserModel:
    query = select(UserModel).where(UserModel.telegram_id == telegram_user.id)

    user_result = await async_session.execute(query)

    user: UserModel | None = user_result.scalars().first()

    if not user:
        user = UserModel(
            telegram_id=telegram_user.id,
            username=telegram_user.username,
            full_name=telegram_user.full_name,
            allowed=False,
        )
        async_session.add(user)
        return user

    user.username = telegram_user.username
    user.full_name = telegram_user.full_name

    return user


async def set_allowed_user_by_telegram_id(
    async_session: AsyncSession,
    telegram_id: int,
    is_allowed: bool,
) -> UserModel:
    user = await get_user_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_id,
    )

    if not user:
        user = UserModel(
            telegram_id=telegram_id,
            allowed=is_allowed,
        )
        async_session.add(user)
        return user

    user.allowed = is_allowed
    return user


async def is_allowed_by_telegram_id(
    async_session: AsyncSession,
    telegram_id: int,
) -> bool:
    query = select(UserModel).where(
        UserModel.telegram_id == telegram_id,
        UserModel.allowed == true(),
    )

    query_result = await async_session.execute(query)

    return query_result.scalars().first() is not None


async def add_used_tokens_by_telegram_id(
    async_session: AsyncSession,
    telegram_id: int,
    tokens_used: int,
) -> None:
    user = await get_user_by_telegram_id(
        async_session=async_session,
        telegram_id=telegram_id,
    )

    if not user:
        return

    user.tokens_used += tokens_used
