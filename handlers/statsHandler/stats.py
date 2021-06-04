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
    if message.text.lower() in map(lambda x: str(x).lower(), stats_types_keyboard.TYPES):
        stats_obj['Type'] = message.text.lower()
        if message.text.lower() == 'chart':
            await DiagramStats.kind.set()
            await message.answer("Select kind of chart.", reply_markup=chart_kinds_keyboard.chart_kinds_kb)
        elif message.text.lower() == '.xlsx':
            await FileStats.period.set()
            await message.answer("Select period.", reply_markup=stats_period_keyboard.stats_period_kb)
        elif message.text.lower() == 'text':
            await TextStats.period.set()
            await message.answer("Select period.", reply_markup=stats_period_keyboard.stats_period_kb)

    else:
        await message.answer('Choose from keyboard.', reply_markup=stats_types_keyboard.st_types_kb)


# CHARTS
@dp.message_handler(state=DiagramStats.kind)
async def process_chart_kind(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), chart_kinds_keyboard.KINDS):
        stats_obj['Kind'] = message.text.lower()
        await message.answer("Select period.", reply_markup=stats_period_keyboard.stats_period_kb)
        await DiagramStats.next()
    else:
        await message.answer('Choose from keyboard.', reply_markup=chart_kinds_keyboard.chart_kinds_kb)


@dp.message_handler(state=DiagramStats.period)
async def process_chart_period(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), stats_period_keyboard.PERIODS):
        stats_obj['Period'] = message.text.lower()
        print(stats_obj)
        # res = create_chart(stats_obj)
        await create_pie_chart(message, message.text)
        await state.finish()
        await message.answer(f"Your {stats_obj['Kind']} for {stats_obj['Period']}",
                             reply_markup=commands_keyboard.commands_kb)
    else:
        await message.answer('Choose from keyboard.', reply_markup=stats_period_keyboard.stats_period_kb)



# TEXT
@dp.message_handler(state=TextStats.period)
async def process_text_result(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), stats_period_keyboard.PERIODS):
        stats_obj['Period'] = message.text.lower()
        await state.finish()
        await message.answer(f"Your text stats for {message.text}.", reply_markup=commands_keyboard.commands_kb)
    else:
        await message.answer('Choose from keyboard.', reply_markup=stats_period_keyboard.stats_period_kb)



# FILE
@dp.message_handler(state=FileStats.period)
async def process_file_result(message: types.Message, state: FSMContext):
    if message.text.lower() in map(lambda x: str(x).lower(), stats_period_keyboard.PERIODS):
        stats_obj['Period'] = message.text.lower()
        await state.finish()
        await message.answer(f"Your file stats for {message.text}.", reply_markup=commands_keyboard.commands_kb)
    else:
        await message.answer('Choose from keyboard.', reply_markup=stats_period_keyboard.stats_period_kb)
