from aiogram import types
from loader import dp

CATEGORIES = ['Food', 'Transport', 'Education', 'Utiliries', 'Tobacco', 'Other']

category_kb = types.inline_keyboard.InlineKeyboardMarkup(row_width=3)
for category in CATEGORIES:
    btn = types.inline_keyboard.InlineKeyboardButton(category, callback_data='process_category_btn')
    category_kb.insert(btn)



# @dp.callback_query_handler(func=lambda c: c.data == 'process_food_btn')
# async def process_food_btn(callback_query: types.CallbackQuery):
#     await callback_query.answer(callback_query.id)
#     await callback_query.message.answer(callback_query.from_user.id, 'Нажата первая кнопка!')