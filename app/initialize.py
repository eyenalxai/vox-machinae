from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine

from app.app_settings import settings
from app.config.log import logger


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
    dispatcher.startup.register(callback=on_startup)
    dispatcher.shutdown.register(callback=on_shutdown)

    return dispatcher
