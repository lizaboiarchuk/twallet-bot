from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.new_expense_state import NewExpense
from keyboards import category_keyboard,currency_keyboard,date_keyboard


@dp.message_handler(Command('expense'), state=None)
async def process_new_income(message: types.Message):
    await message.answer('Adding new expense\n''Enter sum: ')
    await NewExpense.sum.set()


@dp.message_handler(state=NewExpense.sum)
async def process_income_sum(message: types.Message, state: FSMContext):
    await message.answer('Сategory: ', reply_markup=category_keyboard.category_kb)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.category)
async def process_income_source(message: types.Message, state: FSMContext):
    await message.answer('Name: ')
    await NewExpense.next()


@dp.message_handler(state=NewExpense.name)
async def process_income_source(message: types.Message, state: FSMContext):
    await message.answer('Date: ', reply_markup=date_keyboard.date_kb)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.date)
async def process_income_date(message: types.Message, state: FSMContext):
    await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?', reply_markup=currency_keyboard.currency_kb)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.currency)
async def process_income_currency(message: types.Message, state: FSMContext):
    await message.answer("Expense saved.")
    await state.finish()




