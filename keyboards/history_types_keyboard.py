from aiogram import types
from loader import dp

TYPES = ['Incomes', 'Expenses', 'All']

hist_types_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3)
for type in TYPES:
    btn = types.inline_keyboard.InlineKeyboardButton(type, callback_data='process_hist_type_btn')
    hist_types_kb.insert(btn)