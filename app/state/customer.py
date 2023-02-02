from aiogram.fsm.state import State, StatesGroup


class MainCustomerSG(StatesGroup):
    main_menu = State()


class SelectTextModelSG(StatesGroup):
    select_text_model_menu = State()


class TextModelSG(StatesGroup):
    davinci = State()
    curie = State()
    babbage = State()
    ada = State()


class ImageFromTextSG(StatesGroup):
    image_model = State()
