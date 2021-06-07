from aiogram.dispatcher.filters.state import StatesGroup, State


class NewExpense(StatesGroup):
    sum = State()
    category_kb = State()
    category_other = State()
    name = State()
    date_kb = State()
    date_other = State()
    currency_kb = State()
    currency_other = State()
