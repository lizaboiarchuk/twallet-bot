import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
from loader import dp
from creators.history import history_creator
from states.history_state import ShowHistory
from creators.history import history_creator
from aiogram_calendar import simple_cal_callback, SimpleCalendar
from keyboards import commands_keyboard, history_types_keyboard, history_period_keyboard

hist_query = {}


@dp.message_handler(Command('history'), state=None)
async def process_history(message: types.Message):
    hist_query.clear()
    await message.answer('Select type: ', reply_markup=history_types_keyboard.hist_types_kb)
    await ShowHistory.type.set()


@dp.message_handler(state=ShowHistory.type)
async def process_type(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), history_types_keyboard.TYPES):
        hist_query['Type'] = message.text.lower()
        await message.answer('Select period:', reply_markup=history_period_keyboard.hist_periods_kb)
        await ShowHistory.period.set()

    else:
        await message.answer('Choose from keyboard.', reply_markup=history_types_keyboard.hist_types_kb)


@dp.message_handler(state=ShowHistory.period)
async def process_period(message: types.Message, state: FSMContext):
    if message.text.lower() == 'other':
        hist_query['Period'] = 'other'
        await ShowHistory.period_start.set()
        await message.answer('Choose start date: ', reply_markup=await SimpleCalendar().start_calendar())


    elif message.text.lower() in map(lambda x: str(x).lower(), history_period_keyboard.PERIODS):
        hist_query['Period'] = message.text.lower()
        res = await history_creator.get_history(hist_query, message.chat.id)
        await message.answer(res, reply_markup=commands_keyboard.commands_kb)
        await state.finish()
        print('\nNEW HISTORY QUERY CREATED.')
    else:
        await message.answer('Choose from keyboard.', reply_markup=history_period_keyboard.hist_periods_kb)


@dp.callback_query_handler(simple_cal_callback.filter(), state=ShowHistory.period_start)
async def process_start_calendar(callback_query: CallbackQuery, callback_data: dict):
    print('in fisrst calendar')
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}')
        hist_query['date_start'] = f'{date.strftime("%d/%m/%Y")}'
        await ShowHistory.period_end.set()
        await callback_query.message.answer(f'Choose end date:', reply_markup=await SimpleCalendar().start_calendar())


@dp.callback_query_handler(simple_cal_callback.filter(), state=ShowHistory.period_end)
async def process_end_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}')

        start_tokens = hist_query['date_start'].split('/')
        start_date = datetime.datetime(int(start_tokens[2]), int(start_tokens[1]), int(start_tokens[0]))

        if date <= start_date:
            await callback_query.message.answer('End date should be ahead of start date. Choose again. ',
                                                reply_markup=await SimpleCalendar().start_calendar())
        else:
            hist_query['date_end'] = f'{date.strftime("%d/%m/%Y")}'
            res = await history_creator.get_history(hist_query, callback_query.message.chat.id)
            await callback_query.message.answer(res, reply_markup=commands_keyboard.commands_kb)
            await dp.current_state().finish()
