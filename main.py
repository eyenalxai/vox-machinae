from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.app_settings import settings
from app.initialize import initialize_dispatcher
from app.util.healthcheck import health


def start_bot(dispatcher: Dispatcher, bot: Bot) -> None:
    if settings.poll_type == "WEBHOOK":
        app = web.Application()
        SimpleRequestHandler(dispatcher=dispatcher, bot=bot).register(
            app,
            path=settings.main_bot_path,
        )
        setup_application(app, dispatcher, bot=bot)
        app.add_routes([web.get("/health", health)])
        web.run_app(app, host=settings.host, port=settings.port)

    if settings.poll_type == "POLLING":
        dispatcher.run_polling(bot, skip_updates=True)


def main() -> None:
    bot = Bot(settings.telegram_token, parse_mode="HTML")
    dispatcher = initialize_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
