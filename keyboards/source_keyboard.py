from aiogram import types
from loader import dp

SOURCES = ['Salary', 'Scholarship', 'Other']

source_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=2)
for source in SOURCES:
    btn = types.inline_keyboard.InlineKeyboardButton(source, callback_data='process_source_btn')
    source_kb.insert(btn)