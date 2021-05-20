from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.show_stats_state import ShowStats
from keyboards import source_keyboard, date_keyboard, currency_keyboard, stats_types_keyboard, commands_keyboard


@dp.message_handler(Command('stats'), state=None)
async def process_new_stats(message: types.Message):
    await message.answer('Retrieving statistics. Select type.', reply_markup=stats_types_keyboard.st_types_kb)
    await ShowStats.type.set()

@dp.message_handler(state=ShowStats.type)
async def process_income_sum(message: types.Message, state: FSMContext):
    print(message)
    await message.answer('Your staistics.', reply_markup=commands_keyboard.commands_kb)
    await state.finish()
