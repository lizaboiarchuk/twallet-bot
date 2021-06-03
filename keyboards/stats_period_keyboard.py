from aiogram import types
from loader import dp
from states import show_stats_state
import handlers


PERIODS = ['Week', 'Month', 'Year']

stats_period_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=1)
for period in PERIODS:
    btn = types.inline_keyboard.InlineKeyboardButton(period, callback_data=f'stats_period_{period}')
    stats_period_kb.insert(btn)

btn = types.inline_keyboard.InlineKeyboardButton('Cancel', callback_data=f'stats_period_cancel_button')
stats_period_kb.insert(btn)



@dp.callback_query_handler(lambda c: c.data.startswith('stats_period_'), state='*')
async def process_hist_types(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'stats_period_cancel_button':
        await handlers.defaultHandler.default.cancel_handler(message, state=dp.current_state())
        return
    message.text = callback_query.data.replace('stats_period_', '')
    state_name = await dp.current_state().get_state()

    if state_name in show_stats_state.TextStats.all_states_names:
        await handlers.statsHandler.stats.process_text_result(message, state=dp.current_state())

    elif state_name in show_stats_state.FileStats.all_states_names:
        await handlers.statsHandler.stats.process_file_result(message, state=dp.current_state())

    elif state_name in show_stats_state.DiagramStats.all_states_names:
        await handlers.statsHandler.stats.process_chart_period(message, state=dp.current_state())






