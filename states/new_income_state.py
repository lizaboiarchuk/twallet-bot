from aiogram.dispatcher.filters.state import StatesGroup, State


class NewIncome(StatesGroup):
    sum = State()
    source_kb = State()
    source_other = State()
    date_kb = State()
    date_other = State()
    currency_kb = State()
    currency_other = State()
