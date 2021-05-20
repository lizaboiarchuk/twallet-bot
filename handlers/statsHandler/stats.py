from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.show_stats_state import ShowStats
from keyboards import source_keyboard, date_keyboard, currency_keyboard


@dp.message_handler(Command('stats'), state=None)
async def process_new_income(message: types.Message):
    await message.answer('Retrieving statistics. Select type.')
    await ShowStats.type.set()