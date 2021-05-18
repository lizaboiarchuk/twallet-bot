from config import TOKEN
import logging
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_grating(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hi!\n')

@dp.message_handler(commands=['help'])
async def process_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'See the manual:\n')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)