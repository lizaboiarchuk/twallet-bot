from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.new_income_state import NewIncome
from keyboards import source_keyboard, date_keyboard, currency_keyboard, commands_keyboard


@dp.message_handler(Command('income'), state=None)
async def process_new_income(message: types.Message):
    await message.answer('Adding new income\n''Enter sum: ')
    await NewIncome.sum.set()


@dp.message_handler(state=NewIncome.sum)
async def process_income_sum(message: types.Message, state: FSMContext):
    await message.answer('Source: ', reply_markup=source_keyboard.source_kb)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.source)
async def process_income_source(message: types.Message, state: FSMContext):
    await message.answer('Date: ', reply_markup=date_keyboard.date_kb)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.date)
async def process_income_date(message: types.Message, state: FSMContext):
    await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?', reply_markup=currency_keyboard.currency_kb)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.currency)
async def process_income_currency(message: types.Message, state: FSMContext):
    await message.answer("Income saved.", reply_markup=commands_keyboard.commands_kb)
    await state.finish()




