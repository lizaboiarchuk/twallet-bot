from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from states.new_expense_state import NewExpense
from keyboards import category_keyboard,currency_keyboard,date_keyboard, commands_keyboard

new_expense_obj = {}


@dp.message_handler(Command('expense'), state=None)
async def process_new_expense(message: types.Message):
    new_expense_obj.clear()
    await message.answer('Adding new expense\n''Enter sum: ')
    await NewExpense.sum.set()


@dp.message_handler(state=NewExpense.sum)
async def process_sum(message: types.Message, state: FSMContext):
    new_expense_obj['Sum'] = message.text
    await NewExpense.next()
    await message.answer('Сategory: ', reply_markup=category_keyboard.category_kb)


@dp.message_handler(state=NewExpense.category_kb)
async def process_category_kb(message: types.Message, state: FSMContext):
    if message.text == 'Other':
        await message.answer('Enter category: ')
        await NewExpense.category_other.set()
    else:
        new_expense_obj['Category'] = message.text
        await message.answer('Enter name: ')
        await NewExpense.name.set()


@dp.message_handler(state=NewExpense.category_other)
async def process_category_other(message: types.Message, state: FSMContext):
    new_expense_obj['Category'] = message.text
    await message.answer('Enter name: ')
    await NewExpense.name.set()


@dp.message_handler(state=NewExpense.name)
async def process_name(message: types.Message, state: FSMContext):
    new_expense_obj['Name'] = message.text
    await message.answer('Date: ', reply_markup=date_keyboard.date_kb)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.date_kb)
async def process_date_kb(message: types.Message, state: FSMContext):
    if message.text == 'Other':
        await message.answer("Enter income's date:")
        await NewExpense.date_other.set()
    else:
        new_expense_obj['Date'] = 'today'
        await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?',
                             reply_markup=currency_keyboard.currency_kb)
        await NewExpense.currency_kb.set()


@dp.message_handler(state=NewExpense.date_other)
async def process_date_other(message: types.Message, state: FSMContext):
    new_expense_obj['Date'] = message.text
    await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?', reply_markup=currency_keyboard.currency_kb)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.currency_kb)
async def process_currency_kb(message: types.Message, state: FSMContext):
    if message.text == 'Other':
        await message.answer("Choose other currency: ")
        await NewExpense.currency_other.set()
    else:
        new_expense_obj['Currency'] = currency_keyboard.CURRENCY
        await message.answer("Expense saved.", reply_markup=commands_keyboard.commands_kb)
        await state.finish()
        print("NEW EXPENSE CREATED.")
        print(new_expense_obj)


@dp.message_handler(state=NewExpense.currency_other)
async def process_currency_other(message: types.Message, state: FSMContext):
    new_expense_obj['Currency'] = message.text
    await message.answer("Expense saved.", reply_markup=commands_keyboard.commands_kb)
    await state.finish()
    print("NEW EXPENSE CREATED.")
    print(new_expense_obj)






