from aiogram import types
from loader import dp
from states import history_state
import handlers

TYPES = ['Incomes', 'Expenses', 'All']

hist_types_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3)
for type in TYPES:
    btn = types.inline_keyboard.InlineKeyboardButton(type, callback_data=f'hist_type_{type}')
    hist_types_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'hist_type_cancel_button')
hist_types_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('hist_type_'), state=history_state.ShowHistory.type)
async def process_hist_types(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'hist_type_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    message.text = callback_query.data.replace('hist_type_', '')
    await handlers.historyHandler.history.process_type(message, state=dp.current_state())
