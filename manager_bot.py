from aiogram import Bot

from app.util.dispatcher.initialize_manager import initialize_manager_dispatcher
from app.util.lifecycle.start import start_bot
from app.util.settings.shared import shared_settings


def main() -> None:
    bot = Bot(shared_settings.telegram_token, parse_mode="HTML")
    dispatcher = initialize_manager_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
