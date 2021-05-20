from loader import dp
from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Command
from keyboards import commands_keyboard
from aiogram.utils.markdown import *



@dp.message_handler(Command('start'))
async def process_start(message: types.Message):
    await message.answer('Hi!\n'
                         'This is tWallet - money tracker bot.\n'
                         'See the manual:\n'
                         '/income - adding new income\n'
                         '/expense - adding new expense\n'
                         '/balance - check current balance\n'
                         '/stats - show statistics\n'
                         '/history - see the history\n',
                         reply_markup=commands_keyboard.commands_kb)



@dp.message_handler(Command('help'))
async def process_help(message: types.Message):
    await message.answer('/income - adding new income\n'
                         '/expense - adding new expense\n'
                         '/balance - check current balance\n'
                         '/stats - show statistics\n'
                         '/history - see the history\n',
                         reply_markup=commands_keyboard.commands_kb)


@dp.message_handler(Command('balance'))
async def process_balance(message: types.Message):
    await message.answer(text(bold("Current balance: 0")),
                         reply_markup=commands_keyboard.commands_kb, parse_mode=ParseMode.MARKDOWN)