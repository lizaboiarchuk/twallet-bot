from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from loader import dp
from states.new_income_state import NewIncome
from keyboards import source_keyboard, date_keyboard, currency_keyboard, commands_keyboard, another_curr_keyboard
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from datetime import date
import aiohttp
from config import SERVER_URL

new_income_obj = {}


@dp.message_handler(Command('income'), state=None)
async def process_new_income(message: types.Message):
    new_income_obj.clear()
    await message.answer('Adding new income\n''Enter sum: ')
    await NewIncome.sum.set()


@dp.message_handler(state=NewIncome.sum)
async def process_sum(message: types.Message, state: FSMContext):
    if not str(message.text).replace('.', '', 1).isdigit():
        await message.answer('Sum has to be a number. Enter sum: ')
    else:
        new_income_obj['sum'] = float(message.text)
        await NewIncome.next()
        await message.answer('Source: ', reply_markup=source_keyboard.source_kb)


@dp.message_handler(state=NewIncome.source_kb)
async def process_source_kb(message: types.Message, state: FSMContext):
    if message.text.lower() == 'other':
        await message.answer('Enter source name:')
        await NewIncome.source_other.set()
    elif message.text.lower() in map(lambda x: str(x).lower(), source_keyboard.SOURCES):
        new_income_obj['name'] = message.text.lower()
        await message.answer('Date: ', reply_markup=date_keyboard.date_kb)
        await NewIncome.date_kb.set()
    else:
        await message.answer('Choose from keyboard.', reply_markup=source_keyboard.source_kb)


@dp.message_handler(state=NewIncome.source_other)
async def process_source_other(message: types.Message, state: FSMContext):
    new_income_obj['name'] = message.text.lower()
    await message.answer('Date: ', reply_markup=date_keyboard.date_kb)
    await NewIncome.next()


@dp.message_handler(state=NewIncome.date_kb)
async def process_date_kb(message: types.Message, state: FSMContext):
    if message.text.lower() == 'other':
        await message.answer("Enter income's date:", reply_markup=await SimpleCalendar().start_calendar())
        await NewIncome.date_other.set()
    elif message.text.lower() == 'today':
        today = date.today()
        new_income_obj['date'] = f'{today.strftime("%d/%m/%Y")}'
        await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?',
                             reply_markup=currency_keyboard.currency_kb)
        await NewIncome.currency_kb.set()
    else:
        await message.answer('Choose from keyboard.', reply_markup=date_keyboard.date_kb)


@dp.callback_query_handler(simple_cal_callback.filter(), state=NewIncome.date_other)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}')
        new_income_obj['date'] = f'{date.strftime("%d/%m/%Y")}'
        await callback_query.message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?',
                                            reply_markup=currency_keyboard.currency_kb)
        await NewIncome.next()


@dp.message_handler(state=NewIncome.currency_kb)
async def process_currency_kb(message: types.Message, state: FSMContext):
    if message.text.lower() == 'other':
        await message.answer("Choose other currency. ", reply_markup=another_curr_keyboard.other_currencies_kb)
        await NewIncome.currency_other.set()
    elif message.text.lower() == currency_keyboard.CURRENCIES[0].lower():
        new_income_obj['Currency'] = currency_keyboard.CURRENCY.upper()
        new_income_obj['user_id'] = message.chat.id

        async with aiohttp.ClientSession() as session:
            async with session.post(f'{SERVER_URL}/incomes', json=new_income_obj) as resp:
                print("inc reqw")
                print(resp.status)
                print(await resp.text())
        await message.answer("Income saved.", reply_markup=commands_keyboard.commands_kb)
        await state.finish()
        print("NEW INCOME CREATED.")
        print(new_income_obj)
    else:
        await message.answer('Choose from keyboard.', reply_markup=currency_keyboard.currency_kb)


@dp.message_handler(state=NewIncome.currency_other)
async def process_currency_other(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), another_curr_keyboard.CURRENCIES):
        new_income_obj['Currency'] = message.text.upper()
        print("NEW INCOME CREATED.")
        new_income_obj['user_id'] = message.chat.id
        print(new_income_obj)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'f{SERVER_URL}/incomes', json=new_income_obj) as resp:
                print(resp.status)
                print(await resp.text())
        await message.answer("Income saved.", reply_markup=commands_keyboard.commands_kb)
        await state.finish()

    else:
        await message.answer('Choose from keyboard.', reply_markup=another_curr_keyboard.other_currencies_kb)
