from aiogram import Dispatcher

from app.middleware.admin import filter_non_admin
from app.route.admin.admin import admin_router
from app.route.customer.text import text_router
from app.util.dispatcher.shared_initialize import initialize_shared_dispatcher


def initialize_admin_dispatcher() -> Dispatcher:
    dispatcher = initialize_shared_dispatcher()
    dispatcher.include_router(admin_router)
    text_router.message.middleware(filter_non_admin)  # type: ignore
    return dispatcher
