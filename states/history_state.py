from aiogram.dispatcher.filters.state import StatesGroup, State

class ShowHistory(StatesGroup):
    type = State()
    period = State()