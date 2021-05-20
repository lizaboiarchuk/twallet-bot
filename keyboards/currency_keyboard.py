from aiogram import types
from loader import dp
from config import CURRENCY

CURRENCIES = [CURRENCY, 'Other']

currency_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=2)
for curr in CURRENCIES:
    btn = types.inline_keyboard.InlineKeyboardButton(curr, callback_data='process_currency_btn')
    currency_kb.insert(btn)