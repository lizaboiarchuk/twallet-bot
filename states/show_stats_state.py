from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowStats(StatesGroup):
    type = State()


class DiagramStats(StatesGroup):
    kind = State()  # krug/stovp
    period = State()  # w/m/y


class TextStats(StatesGroup):
    period = State()


class FileStats(StatesGroup):
    period = State()
