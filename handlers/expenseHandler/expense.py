from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.new_expense_state import NewExpense

main_curr = 'UAH'

@dp.message_handler(Command('expense'), state=None)
async def process_new_income(message: types.Message):
    await message.answer('Adding new expense\n''Enter sum: ')
    await NewExpense.sum.set()


@dp.message_handler(state=NewExpense.sum)
async def process_income_sum(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Food", "Transport", "Education")
    markup.add("Cigarettes", "Utilities", "Other")
    await message.answer('Сategory: ', reply_markup=markup)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.category)
async def process_income_source(message: types.Message, state: FSMContext):
    await message.answer('Name: ')
    await NewExpense.next()


@dp.message_handler(state=NewExpense.name)
async def process_income_source(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add("Today", "Select other")
    await message.answer('Date: ', reply_markup=markup)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.date)
async def process_income_date(message: types.Message, state: FSMContext):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True, one_time_keyboard=True)
    markup.add(f"{main_curr}", "Other")
    await message.answer(f'Current currency {main_curr}. Change it?', reply_markup=markup)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.currency)
async def process_income_currency(message: types.Message, state: FSMContext):
    await message.answer("Expense saved.")
    await state.finish()




