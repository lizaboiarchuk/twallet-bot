from aiogram import types
from loader import dp
from config import CURRENCY
import states, handlers

CURRENCIES = [CURRENCY, 'Other']

currency_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=2)
for curr in CURRENCIES:
    btn = types.inline_keyboard.InlineKeyboardButton(curr, callback_data=f'currency_{curr==CURRENCY and "Current" or "Other"}')
    currency_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'currency_cancel_button')
currency_kb.insert(btn)

@dp.callback_query_handler(lambda c: c.data.startswith('currency'), state = states.new_income_state.NewIncome.currency_kb)
async def process_income_curr(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'currency_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    elif callback_query.data == 'currency_Current':
        message.text = 'Current'
    elif callback_query.data == 'currency_Other':
        message.text = 'Other'
    await handlers.incomeHandler.income.process_currency_kb(message, state=dp.current_state())


@dp.callback_query_handler(lambda c: c.data.startswith('currency'), state = states.new_expense_state.NewExpense.currency_kb)
async def process_expense_curr(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'currency_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    elif callback_query.data == 'currency_Current':
        message.text = 'Current'
    elif callback_query.data == 'currency_Other':
        message.text = 'Other'
    await handlers.expenseHandler.expense.process_currency_kb(message, state=dp.current_state())



