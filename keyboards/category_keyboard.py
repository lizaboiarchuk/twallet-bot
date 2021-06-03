from aiogram import types
from loader import dp
import states, handlers

CATEGORIES = ['Food', 'Transport', 'Education', 'Utilities', 'Tobacco', 'Other']

category_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3)
for category in CATEGORIES:
    btn = types.inline_keyboard.InlineKeyboardButton(category, callback_data=f'category_{category}')
    category_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'category_cancel_button')
category_kb.insert(btn)

@dp.callback_query_handler(lambda c: c.data.startswith('category'), state = states.new_expense_state.NewExpense.category_kb)
async def process_source_btn(callback_query: types.CallbackQuery):
    message = callback_query.message

    if callback_query.data == 'category_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    elif callback_query.data != 'category_Other':
        message.text = callback_query.data.replace('category_', '')
    else:
        message.text = 'Other'
    await handlers.expenseHandler.expense.process_category_kb(message, state=dp.current_state())

