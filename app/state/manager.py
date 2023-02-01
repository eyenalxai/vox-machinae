from aiogram.fsm.state import State, StatesGroup


class MainManagerSG(StatesGroup):
    menu = State()
    allow_user = State()
    disallow_user = State()
