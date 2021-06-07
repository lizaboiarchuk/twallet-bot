from datetime import date
from config import SERVER_URL
import aiohttp
from utils.currency_codes import CURRENCY_CODES
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from loader import dp
from states.new_expense_state import NewExpense
from keyboards import category_keyboard, currency_keyboard, date_keyboard, commands_keyboard, another_curr_keyboard
from aiogram_calendar import simple_cal_callback, SimpleCalendar

new_expense_obj = {}


@dp.message_handler(Command('expense'), state=None)
async def process_new_expense(message: types.Message):
    new_expense_obj.clear()
    await message.answer('Adding new expense\n''Enter sum: ')
    await NewExpense.sum.set()


@dp.message_handler(state=NewExpense.sum)
async def process_sum(message: types.Message, state: FSMContext):
    if not str(message.text).replace('.', '', 1).isdigit():
        await message.answer('Sum has to be a number. Enter sum: ')
    else:
        new_expense_obj['sum'] = float(message.text)
        await NewExpense.next()
        await message.answer('Сategory: ', reply_markup=category_keyboard.category_kb)


@dp.message_handler(state=NewExpense.category_kb)
async def process_category_kb(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), category_keyboard.CATEGORIES):
        new_expense_obj['category'] = message.text.lower()
        await message.answer('Enter name: ')
        await NewExpense.name.set()
    elif message.text.lower() == 'other':
        await message.answer('Enter category: ')
        await NewExpense.category_other.set()
    else:
        await message.answer('Choose from keyboard.', reply_markup=category_keyboard.category_kb)


@dp.message_handler(state=NewExpense.category_other)
async def process_category_other(message: types.Message, state: FSMContext):
    new_expense_obj['category'] = message.text.lower()
    await message.answer('Enter name: ')
    await NewExpense.name.set()


@dp.message_handler(state=NewExpense.name)
async def process_name(message: types.Message, state: FSMContext):
    new_expense_obj['name'] = message.text.lower()
    await message.answer('Date: ', reply_markup=date_keyboard.date_kb)
    await NewExpense.next()


@dp.message_handler(state=NewExpense.date_kb)
async def process_date_kb(message: types.Message, state: FSMContext):
    if message.text.lower() == 'other':
        await message.answer("Enter income's date:", reply_markup=await SimpleCalendar().start_calendar())
        await NewExpense.date_other.set()
    elif message.text.lower() == 'today':
        today = date.today()
        new_expense_obj['date'] = f'{today.strftime("%d/%m/%Y")}'
        await message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?',
                             reply_markup=currency_keyboard.currency_kb)
        await NewExpense.currency_kb.set()
    else:
        await message.answer('Choose from keyboard.', reply_markup=date_keyboard.date_kb)


@dp.callback_query_handler(simple_cal_callback.filter(), state=NewExpense.date_other)
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}')
        new_expense_obj['date'] = f'{date.strftime("%d/%m/%Y")}'
        await callback_query.message.answer(f'Current currency {currency_keyboard.CURRENCY}. Change it?',
                                            reply_markup=currency_keyboard.currency_kb)
        await NewExpense.next()


@dp.message_handler(state=NewExpense.currency_kb)
async def process_currency_kb(message: types.Message, state: FSMContext):
    if message.text.lower() == 'other':
        await message.answer("Choose other currency. ", reply_markup=another_curr_keyboard.other_currencies_kb)
        await NewExpense.currency_other.set()
    elif message.text.lower() == currency_keyboard.CURRENCIES[0].lower():
        new_expense_obj['currency'] = CURRENCY_CODES[message.text.upper()]
        new_expense_obj['user_id'] = message.chat.id
        async with aiohttp.ClientSession() as session:
            async with session.post(f'f{SERVER_URL}/outcomes', json=new_expense_obj) as resp:
                print(resp.status)
        await message.answer("Expense saved.", reply_markup=commands_keyboard.commands_kb)
        await state.finish()
    else:
        await message.answer('Choose from keyboard.', reply_markup=currency_keyboard.currency_kb)


@dp.message_handler(state=NewExpense.currency_other)
async def process_currency_other(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), another_curr_keyboard.CURRENCIES):
        new_expense_obj['currency'] = CURRENCY_CODES[message.text.upper()]
        new_expense_obj['user_id'] = message.chat.id
        async with aiohttp.ClientSession() as session:
            async with session.post(f'f{SERVER_URL}/outcomes', json=new_expense_obj) as resp:
                print(resp.status)
        await message.answer("Expense saved.", reply_markup=commands_keyboard.commands_kb)
        await state.finish()
    else:
        await message.answer('Choose from keyboard.', reply_markup=another_curr_keyboard.other_currencies_kb)
