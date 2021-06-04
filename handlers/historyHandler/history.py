from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.history_state import ShowHistory
from keyboards import source_keyboard, date_keyboard, currency_keyboard, commands_keyboard, history_types_keyboard, history_period_keyboard

hist_query = {}

@dp.message_handler(Command('history'), state=None)
async def process_history(message: types.Message):
    hist_query.clear()
    await message.answer('Select type: ', reply_markup=history_types_keyboard.hist_types_kb)
    await ShowHistory.type.set()

@dp.message_handler(state=ShowHistory.type)
async def process_type(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), history_types_keyboard.TYPES):
        hist_query['Type'] = message.text.lower()
        await message.answer('Select period:', reply_markup=history_period_keyboard.hist_periods_kb)
        await ShowHistory.next()
    else:
        await message.answer('Choose from keyboard.', reply_markup=history_types_keyboard.hist_types_kb)



@dp.message_handler(state=ShowHistory.period)
async def process_period(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), history_period_keyboard.PERIODS):
        hist_query['Period'] = message.text.lower()
        await message.answer('history \n-\n-\n-\n', reply_markup=commands_keyboard.commands_kb)
        await state.finish()
        print('\nNEW HISTORY QUERY CREATED.')
        print(hist_query)
    else:
        await message.answer('Choose from keyboard.', reply_markup=history_period_keyboard.hist_periods_kb)




