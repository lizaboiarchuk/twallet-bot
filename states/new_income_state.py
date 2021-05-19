from aiogram.dispatcher.filters.state import StatesGroup, State

class NewIncome(StatesGroup):
    sum = State()
    source = State()
    date = State()
    currency = State()