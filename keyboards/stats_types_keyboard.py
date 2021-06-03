from aiogram import types
from loader import dp
import states
import handlers

TYPES = ['Chart', '.XLSX', 'Text']

st_types_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for type in TYPES:
    btn = types.inline_keyboard.InlineKeyboardButton(type, callback_data=f'process_st_type_btn_{type}')
    st_types_kb.insert(btn)
btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'process_st_type_cancel_button')
st_types_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('process_st_type'), state = states.show_stats_state.ShowStats.type)
async def process_source_btn(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'process_st_type_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    else:
        message.text = callback_query.data.replace('process_st_type_btn_', '')
        await handlers.statsHandler.stats.process_type(message, state=dp.current_state())


