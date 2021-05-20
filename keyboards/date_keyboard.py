from aiogram import types
from loader import dp

DATES = ['Today', 'Other']

date_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=2)
for date in DATES:
    btn = types.inline_keyboard.InlineKeyboardButton(date, callback_data='process_date_btn')
    date_kb.insert(btn)