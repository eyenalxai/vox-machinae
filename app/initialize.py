from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine

from app.app_settings import settings
from app.config.log import logger
from app.middleware.access import filter_non_allowed
from app.middleware.admin import filter_non_admin
from app.middleware.database_session import get_async_database_session
from app.middleware.text import filter_not_text
from app.middleware.user import filter_non_user, update_user
from app.route.admin import admin_router
from app.route.start import start_router
from app.route.text import text_router
from app.util.openai.text_model import openai_text_wrapper


async def on_startup(bot: Bot) -> None:
    if settings.poll_type == "WEBHOOK":
        webhook_url = settings.webhook_url
        await bot.set_webhook(webhook_url)
        logger.info("Webhook set to: %s", webhook_url)


async def on_shutdown(bot: Bot) -> None:
    logger.info("Shutting down...")
    if settings.poll_type == "WEBHOOK":
        await bot.delete_webhook()
        logger.info("Webhook removed")


def initialize_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()

    dispatcher["async_engine"] = create_async_engine(
        url=settings.async_database_url,
        pool_size=settings.database_pool_size,
        pool_pre_ping=True,
    )
    dispatcher["text_prompt"] = openai_text_wrapper()

    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    dispatcher.message.middleware(get_async_database_session)  # type: ignore

    dispatcher.message.middleware(filter_non_user)  # type: ignore
    dispatcher.message.middleware(update_user)  # type: ignore

    dispatcher.include_router(start_router)
    dispatcher.include_router(admin_router)
    dispatcher.include_router(text_router)

    admin_router.message.middleware(filter_non_admin)  # type: ignore

    text_router.message.middleware(filter_non_allowed)  # type: ignore
    text_router.message.middleware(filter_not_text)  # type: ignore

    return dispatcher
