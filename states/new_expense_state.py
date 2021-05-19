from aiogram.dispatcher.filters.state import StatesGroup, State

class NewExpense(StatesGroup):
    sum = State()
    category = State()
    name = State()
    date = State()
    currency = State()