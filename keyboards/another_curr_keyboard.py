from aiogram import types
from loader import dp
from states import new_income_state, new_expense_state
import handlers

CURRENCIES = ['USD', 'EUR', 'JPY', 'GBP', 'CAD', 'CHF', 'AUD', 'CNY', 'NZD']

other_currencies_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3)
for curr in CURRENCIES:
    btn = types.inline_keyboard.InlineKeyboardButton(curr, callback_data=f'other_curr_{curr}')
    other_currencies_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'other_curr_cancel_button')
other_currencies_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('other_curr'), state='*')
async def process_source_btn(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'other_curr_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    message.text = callback_query.data.replace('other_curr_', '')
    state_name = await dp.current_state().get_state()
    if state_name in new_income_state.NewIncome.all_states_names:
        await handlers.incomeHandler.income.process_currency_other(message, state=dp.current_state())
    elif state_name in new_expense_state.NewExpense.all_states_names:
        await handlers.expenseHandler.expense.process_currency_other(message, state=dp.current_state())
