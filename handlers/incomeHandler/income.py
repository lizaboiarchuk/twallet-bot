from aiogram import types
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from loader import dp
from states.new_income_state import NewIncome
from keyboards import source_keyboard, date_keyboard, currency_keyboard, commands_keyboard, another_curr_keyboard

new_income_obj = {}

@dp.message_handler(Command('income'), state=None)
async def process_new_income(message: types.Message):
    new_income_obj.clear()
    await message.answer('Adding new income\n''Enter sum: ')
    await NewIncome.sum.set()


@dp.message_handler(state=NewIncome.sum)
async def process_sum(message: types.Message, state: FSMContext):
    new_income_obj['Sum'] = message.text
    await NewIncome.next()
    await message.answer('Source: ', reply_markup=source_keyboard.source_kb)


@dp.message_handler(state=NewIncome.source_kb)
async def process_source_kb(message: types.Message, state: FSMContext):
    if message.text == 'Other':
        await message.answer('Enter source name:')
        await NewIncome.source_other.set()
    else:
        new_income_obj['Source'] = message.text
        await message.answer('Date: ', reply_markup = date_keyboard.date_kb)
        await NewIncome.date_kb.set()


@dp.message_handler(state=NewIncome.source_other)
async def process_source_other(message: types.Message, state: FSMContext):
    new_income_obj['Source'] = message.text
    await message.answer('Date: ', reply_markup = date_keyboard.date_kb)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.date_kb)
async def process_date_kb(message: types.Message, state: FSMContext):
    if message.text == 'Other':
        await message.answer("Enter income's date:")
        await NewIncome.date_other.set()
    else:
        new_income_obj['Date'] = 'today'
        await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?', reply_markup=currency_keyboard.currency_kb)
        await NewIncome.currency_kb.set()


@dp.message_handler(state=NewIncome.date_other)
async def process_date_other(message: types.Message, state: FSMContext):
    new_income_obj['Date'] = message.text
    await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?', reply_markup=currency_keyboard.currency_kb)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.currency_kb)
async def process_currency_kb(message: types.Message, state: FSMContext):
    if message.text == 'Other':
        await message.answer("Choose other currency. ", reply_markup=another_curr_keyboard.other_currencies_kb)
        await NewIncome.currency_other.set()
    else:
        new_income_obj['Currency'] = currency_keyboard.CURRENCY
        await message.answer("Income saved.", reply_markup=commands_keyboard.commands_kb)
        await state.finish()
        print("NEW INCOME CREATED.")
        print(new_income_obj)


@dp.message_handler(state=NewIncome.currency_other)
async def process_currency_other(message: types.Message, state: FSMContext):
    new_income_obj['Currency'] = message.text
    await message.answer("Income saved.", reply_markup=commands_keyboard.commands_kb)
    await state.finish()
    print("NEW INCOME CREATED.")
    print(new_income_obj)





