from aiogram.dispatcher.filters.state import StatesGroup, State


class ShowHistory(StatesGroup):
    type = State()
    period = State()
    period_keyboard = State()
    period_start = State()
    period_end = State()
