from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.history_state import ShowHistory
from keyboards import source_keyboard, date_keyboard, currency_keyboard, commands_keyboard, history_types_keyboard, history_period_keyboard


@dp.message_handler(Command('history'), state=None)
async def process_new_income(message: types.Message):
    await message.answer('Select type. ', reply_markup=history_types_keyboard.hist_types_kb)
    await ShowHistory.type.set()

@dp.message_handler(state=ShowHistory.type)
async def process_income_sum(message: types.Message, state: FSMContext):
    await message.answer('Select period.', reply_markup=history_period_keyboard.hist_periods_kb)
    await ShowHistory.next()


@dp.message_handler(state=ShowHistory.period)
async def process_income_sum(message: types.Message, state: FSMContext):
    await message.answer('history \n-\n-\n-\n', reply_markup=commands_keyboard.commands_kb)
    await state.finish()


