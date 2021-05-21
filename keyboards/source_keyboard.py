from aiogram import types
from loader import dp
import states
import handlers

SOURCES = ['Salary', 'Scholarship', 'Other']

source_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=2)
for source in SOURCES:
    btn = types.inline_keyboard.InlineKeyboardButton(source, callback_data=f'source_{source}')
    source_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('source'), state = states.new_income_state.NewIncome.source_kb)
async def process_source_btn(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == 'source_Salary':
        message.text = 'Salary'
    elif callback_query.data == 'source_Scholarship':
        message.text = 'Scholarship'
    elif callback_query.data == 'source_Other':
        message.text = 'Other'
    await handlers.incomeHandler.income.process_source_kb(message, state=dp.current_state())


