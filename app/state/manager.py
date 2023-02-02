from aiogram.fsm.state import State, StatesGroup


class MainManagerSG(StatesGroup):
    main_menu = State()


class AccessManagerSG(StatesGroup):
    access_menu = State()
    allow_user = State()
    disallow_user = State()
