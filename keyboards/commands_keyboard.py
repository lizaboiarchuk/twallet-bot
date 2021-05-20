from aiogram import types
from loader import dp
import re
from handlers.incomeHandler.income import *

COMMANDS = ['Income', 'Expense', 'Stats', 'Balance', 'History', 'Help']

commands_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3, )
for command in COMMANDS:
    btn = types.inline_keyboard.InlineKeyboardButton(command, callback_data=f'{command}_command')
    commands_kb.insert(btn)

# @dp.callback_query_handler(lambda c: re.match(r".*(command)$", c.data))
# async def process_command_btn(callback_query: types.CallbackQuery):
#     # print(callback_query.as_json())