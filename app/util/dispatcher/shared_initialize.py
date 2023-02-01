from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine

from app.middleware.database_session import get_async_database_session
from app.util.lifecycle.lifecycle_functions import on_shutdown, on_startup
from app.util.settings.shared import shared_settings


def shared_initialized() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher["async_engine"] = create_async_engine(
        url=shared_settings.async_database_url,
        pool_size=shared_settings.database_pool_size,
        pool_pre_ping=True,
    )

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    dispatcher.message.middleware(get_async_database_session)  # type: ignore

    return dispatcher
