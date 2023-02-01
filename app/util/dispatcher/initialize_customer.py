from aiogram import Dispatcher

from app.middleware.access import filter_non_allowed
from app.middleware.text import filter_not_text
from app.middleware.user import filter_non_user, update_user
from app.route.customer.start import start_router
from app.route.customer.text import text_router
from app.util.dispatcher.shared_initialize import shared_initialized
from app.util.openai.text_model import openai_text_wrapper


def initialize_customer_dispatcher() -> Dispatcher:
    dispatcher = shared_initialized()
    dispatcher["text_prompt"] = openai_text_wrapper()

    dispatcher.message.middleware(filter_non_user)  # type: ignore
    dispatcher.message.middleware(update_user)  # type: ignore

    dispatcher.include_router(start_router)
    dispatcher.include_router(text_router)

    text_router.message.middleware(filter_non_allowed)  # type: ignore
    text_router.message.middleware(filter_not_text)  # type: ignore

    return dispatcher
