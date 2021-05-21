from aiogram import types
from loader import dp
from states import history_state
import handlers

PERIODS = ['Day', 'Week', 'Month', 'Year']

hist_periods_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for period in PERIODS:
    btn = types.inline_keyboard.InlineKeyboardButton(period, callback_data=f'hist_period_{period}')
    hist_periods_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('hist_period_'), state = history_state.ShowHistory.period)
async def process_hist_types(callback_query: types.CallbackQuery):
    message = callback_query.message
    message.text = callback_query.data.replace('hist_period_', '')
    await handlers.historyHandler.history.process_period(message, state=dp.current_state())