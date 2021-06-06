from aiogram import types
from loader import dp
from states import history_state
import handlers

PERIODS = ['Day', 'Week', 'Other']

hist_periods_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for period in PERIODS:
    btn = types.inline_keyboard.InlineKeyboardButton(period, callback_data=f'hist_period_{period}')
    hist_periods_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'hist_period_cancel_button')
hist_periods_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('hist_period_'), state = history_state.ShowHistory.period)
async def process_hist_types(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'hist_period_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    message.text = callback_query.data.replace('hist_period_', '')
    await handlers.historyHandler.history.process_period(message, state=dp.current_state())