from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start using"),
            types.BotCommand("help", "see the manual"),
            types.BotCommand("income", "add new income"),
            types.BotCommand("expense", "add new expense"),
        ]
    )
