from asyncio import sleep

from aiogram import Bot

from app.config.log import logger
from app.util.settings.shared import shared_settings


async def on_startup(bot: Bot) -> None:
    if shared_settings.poll_type == "WEBHOOK":
        webhook_url = shared_settings.webhook_url

        logger.info("Sleeping for 60 seconds...")
        await sleep(60)

        await bot.set_webhook(webhook_url)
        logger.info("Webhook set to: %s", webhook_url)


async def on_shutdown(bot: Bot) -> None:
    logger.info("Shutting down...")
    if shared_settings.poll_type == "WEBHOOK":
        await bot.delete_webhook()
        logger.info("Webhook removed")
