from aiogram import types
from loader import dp
import handlers
from states import new_expense_state, new_income_state

DATES = ['Today', 'Other']

date_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=2)
for date in DATES:
    btn = types.inline_keyboard.InlineKeyboardButton(date, callback_data=f'date_{date}')
    date_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'date_cancel_button')
date_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('date'), state = new_income_state.NewIncome.date_kb)
async def process_income_date(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'date_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    elif callback_query.data == 'date_Today':
        message.text = 'Today'
    elif callback_query.data == 'date_Other':
        message.text = 'Other'
    await handlers.incomeHandler.income.process_date_kb(message, state=dp.current_state())


@dp.callback_query_handler(lambda c: c.data.startswith('date'), state = new_expense_state.NewExpense.date_kb)
async def process_expense_date(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'date_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    elif callback_query.data == 'date_Today':
        message.text = 'Today'
    elif callback_query.data == 'date_Other':
        message.text = 'Other'
    await handlers.expenseHandler.expense.process_date_kb(message, state=dp.current_state())