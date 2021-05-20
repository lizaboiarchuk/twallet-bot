from aiogram import types
from loader import dp

PERIODS = ['Day', 'Week', 'Month', 'Year']

hist_periods_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for period in PERIODS:
    btn = types.inline_keyboard.InlineKeyboardButton(period, callback_data='process_hist_period_btn')
    hist_periods_kb.insert(btn)