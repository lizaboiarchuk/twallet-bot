from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command

@dp.message_handler(Command('start'))
async def process_start(message: types.Message):
    await message.answer('Hi!\n')


@dp.message_handler(Command('help'))
async def process_help(message: types.Message):
    await message.answer('See the manual:\n'
                         '/income - adding new income\n'
                         '/expense - adding new expense\n'
                         '/stat - show statistics\n'
                         )