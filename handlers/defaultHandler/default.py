from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import Command, Text
from keyboards import commands_keyboard
from aiogram.utils.markdown import *
import states



@dp.message_handler(Command('start'))
async def process_start(message: types.Message):
    await message.answer('Hi!\n'
                         'This is tWallet - money tracker bot.\n'
                         'See the manual:\n'
                         '/income - adding new income\n'
                         '/expense - adding new expense\n'
                         '/balance - check current balance\n'
                         '/stats - show statistics\n'
                         '/history - see the history\n',
                         reply_markup=commands_keyboard.commands_kb)



@dp.message_handler(Command('help'))
async def process_help(message: types.Message):
    await message.answer('/income - adding new income\n'
                         '/expense - adding new expense\n'
                         '/balance - check current balance\n'
                         '/stats - show statistics\n'
                         '/history - see the history\n',
                         reply_markup=commands_keyboard.commands_kb)


@dp.message_handler(Command('balance'))
async def process_balance(message: types.Message):
    await message.answer(text(bold("Current balance: 0")),
                         reply_markup=commands_keyboard.commands_kb, parse_mode=ParseMode.MARKDOWN)




@dp.message_handler(Command('cancel'), state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), )
async def cancel_handler(message: types.Message, state: FSMContext):
    id = str(message.chat['id'])
    state_name = (dp.storage.__dict__['data'][id][id]['state'])
    if state_name in states.new_income_state.NewIncome.all_states_names:
        await message.answer('Income cancelled.', reply_markup=commands_keyboard.commands_kb)
    elif state_name in states.new_expense_state.NewExpense.all_states_names:
        await message.answer('Expense cancelled.', reply_markup=commands_keyboard.commands_kb)
    else:
        await message.answer('Action cancelled.', reply_markup=commands_keyboard.commands_kb)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()




