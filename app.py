from loader import bot, storage
from utils.set_bot_commands import set_default_commands


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


async def on_startup(dp):
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
