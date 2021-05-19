from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.new_income_state import NewIncome

main_curr = 'UAH'

@dp.message_handler(Command('income'), state=None)
async def process_new_income(message: types.Message):
    await message.answer('Adding new income\n''Enter sum: ')
    await NewIncome.sum.set()


@dp.message_handler(state=NewIncome.sum)
async def process_income_sum(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Salary", "Scholarship")
    markup.add("Other")
    await message.answer('Source: ', reply_markup=markup)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.source)
async def process_income_source(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Today", "Select other")
    await message.answer('Date: ', reply_markup=markup)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.date)
async def process_income_date(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(f"{main_curr}", "Other")
    await message.answer(f'Current currency {main_curr}. Change it?', reply_markup=markup)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.currency)
async def process_income_currency(message: types.Message, state: FSMContext):
    await message.answer("Income saved.")
    await state.finish()




