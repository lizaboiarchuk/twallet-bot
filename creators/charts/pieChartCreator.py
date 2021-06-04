from pygooglechart import PieChart2D
from aiogram import types
from loader import bot

async def create_pie_chart(message: types.Message, period):
    chart = PieChart2D(700, 400)
    chart.add_data([10, 10, 30, 200])
    chart.set_pie_labels([
        'Budding Chemists',
        'Propane issues',
        'Meth Labs',
        'Attempts to escape morgage',
    ])
    chart.download('chart.png')
    await bot.send_document(chat_id=message.chat.id, document=open('chart.png', 'rb'))
