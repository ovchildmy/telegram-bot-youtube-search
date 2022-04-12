from aiogram import types
from loader import dp


@dp.message_handler(commands='help')
async def bot_help(msg: types.Message):
    text = 'Я - бот для поиска видео с Youtube. Напиши, что хочешь посмотреть и я покажу самое подходящее видео!'
    await msg.answer(text)
