from aiogram import Bot

from app.util.dispatcher.initialize_customer import initialize_customer_dispatcher
from app.util.lifecycle.start import start_bot
from app.util.settings.shared import shared_settings


def main() -> None:
    bot = Bot(shared_settings.telegram_token, parse_mode="HTML")
    dispatcher = initialize_customer_dispatcher()
    start_bot(dispatcher=dispatcher, bot=bot)


if __name__ == "__main__":
    main()
