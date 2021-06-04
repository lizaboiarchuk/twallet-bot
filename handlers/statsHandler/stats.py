from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from states.show_stats_state import *
from keyboards import stats_types_keyboard, commands_keyboard, stats_period_keyboard, chart_kinds_keyboard
from creators.charts.pieChartCreator import create_pie_chart

stats_obj = {}


@dp.message_handler(Command('stats'), state=None)
async def process_new_stats(message: types.Message):
    stats_obj.clear()
    await message.answer('Retrieving statistics. Select type.', reply_markup=stats_types_keyboard.st_types_kb)
    await ShowStats.type.set()


@dp.message_handler(state=ShowStats.type)
async def process_type(message: types.Message, state: FSMContext):
    stats_obj['Type'] = message.text
    if message.text == 'Chart':
        await process_chart_kind_kb(message, state)
        print('chart')
    elif message.text == '.XLSX':
        await process_file_period(message, state)
    elif message.text == 'Text':
        await process_text_period(message, state)


# CHARTS
async def process_chart_kind_kb(message: types.Message, state: FSMContext):
    await DiagramStats.kind.set()
    await message.answer("Select kind of chart.", reply_markup=chart_kinds_keyboard.chart_kinds_kb)


async def process_chart_kind(message: types.Message, state: FSMContext):
    stats_obj['Kind'] = message.text
    await message.answer("Select period.", reply_markup=stats_period_keyboard.stats_period_kb)
    await DiagramStats.next()


async def process_chart_period(message: types.Message, state: FSMContext):
    stats_obj['Period'] = message.text
    print(stats_obj)
    # res = create_chart(stats_obj)
    await create_pie_chart(message, message.text)
    await state.finish()
    await message.answer(f"Your {stats_obj['Kind']} for {stats_obj['Period']}",
                         reply_markup=commands_keyboard.commands_kb)


# TEXT
async def process_text_period(message: types.Message, state: FSMContext):
    await TextStats.period.set()
    await message.answer("Select period.", reply_markup=stats_period_keyboard.stats_period_kb)


async def process_text_result(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Your text stats for {message.text}.", reply_markup=commands_keyboard.commands_kb)


# FILE
async def process_file_period(message: types.Message, state: FSMContext):
    await FileStats.period.set()
    await message.answer("Select period.", reply_markup=stats_period_keyboard.stats_period_kb)


async def process_file_result(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Your file stats for {message.text}.", reply_markup=commands_keyboard.commands_kb)
