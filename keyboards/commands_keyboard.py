from aiogram import types
from loader import dp
import handlers

COMMANDS = ['Income', 'Expense', 'Stats', 'Balance', 'History', 'Help']

commands_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3, )
for command in COMMANDS:
    btn = types.inline_keyboard.InlineKeyboardButton(command, callback_data=f'command_{command}')
    commands_kb.insert(btn)


@dp.callback_query_handler(lambda c: c.data.startswith('command'))
async def process_command_btn(callback_query: types.CallbackQuery):
    if callback_query.data == 'command_Income':
        await handlers.incomeHandler.income.process_new_income(callback_query.message)

    elif callback_query.data == 'command_Expense':
        await handlers.expenseHandler.expense.process_new_expense(callback_query.message)

    elif callback_query.data == 'command_Stats':
        await handlers.statsHandler.stats.process_new_stats(callback_query.message)

    elif callback_query.data == 'command_Balance':
        await handlers.defaultHandler.default.process_balance(callback_query.message)

    elif callback_query.data == 'command_History':
        await handlers.historyHandler.history.process_history(callback_query.message)

    elif callback_query.data == 'command_Help':
        await handlers.defaultHandler.default.process_help(callback_query.message)
