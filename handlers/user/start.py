from aiogram import types
from loader import dp


@dp.message_handler(commands='start')
async def bot_start(msg: types.Message):
    text = 'Напиши, что хочешь посмотреть и я покажу самое подходящее видео!'
    await msg.answer(f'Привет, {msg.from_user.full_name}! ' + text)
