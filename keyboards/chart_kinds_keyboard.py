from aiogram import types
from loader import dp
import states
import handlers

KINDS = ['Pie Chart', 'Column Chart', 'Line Chart']

chart_kinds_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for kind in KINDS:
    btn = types.inline_keyboard.InlineKeyboardButton(kind, callback_data=f'process_char_kind_{kind}')
    chart_kinds_kb.insert(btn)
btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'process_char_kind_cancel_button')
chart_kinds_kb.insert(btn)



@dp.callback_query_handler(lambda c: c.data.startswith('process_char_kind'), state = '*')
async def process_source_btn(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'process_char_kind_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    else:
        message.text = callback_query.data.replace('process_char_kind_', '')
        await handlers.statsHandler.stats.process_chart_kind(message, state=dp.current_state())


