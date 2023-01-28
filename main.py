import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.middleware.filter_not_allowed import filter_not_allowed_user
from app.middleware.filter_not_text import filter_not_text
from app.route.main import main_router
from app.settings import PollType, settings
from app.util.healthcheck import health
from app.util.openai import openai_wrapper


async def on_startup(bot: Bot) -> None:
    if settings.poll_type == PollType.WEBHOOK:
        webhook_url = settings.webhook_url
        await bot.set_webhook(url=webhook_url)
        logging.info("Webhook set to: %s", webhook_url)


async def on_shutdown() -> None:
    logging.info("Shutting down...")


def main() -> None:
    bot = Bot(settings.telegram_token, parse_mode="HTML")

    dispatcher = Dispatcher(events_isolation=SimpleEventIsolation())

    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    dispatcher["create_prompt"] = openai_wrapper()

    dispatcher.message.middleware(filter_not_allowed_user)  # type: ignore
    dispatcher.message.middleware(filter_not_text)  # type: ignore

    dispatcher.include_router(main_router)

    if settings.poll_type == PollType.WEBHOOK:
        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(
            app,
            path=settings.main_bot_path,
        )
        setup_application(app, dispatcher, bot=bot)
        app.add_routes([web.get("/health", health)])
        web.run_app(app, host="0.0.0.0", port=settings.port)

    if settings.poll_type == PollType.POLLING:
        dispatcher.run_polling(bot, skip_updates=True)


if __name__ == "__main__":
    main()
