from aiogram import types
from loader import dp

TYPES = ['Chart', '.XLSX', 'Text']

st_types_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for type in TYPES:
    btn = types.inline_keyboard.InlineKeyboardButton(type, callback_data='process_st_type_btn')
    st_types_kb.insert(btn)