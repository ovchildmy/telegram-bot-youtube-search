from aiogram import Dispatcher, types
from loader import dp
from utils.YouTubeApi import YouTubeApi
from keyboards.inline.video import get_video_kb
from data import config


@dp.message_handler()
async def search_videos(message: types.Message):
    """ обработка запроса пользователя """
    text = message.text

    # сохранение данного запроса
    if len(config.users_data) > 0:
        user_found = False
        for item in config.users_data:
            if item['user_id'] == message.from_user.id:
                user_found = True
                item['text'] = text
        if not user_found:  # если пользователь делает что-то впервые
            data = {
                'user_id': message.from_user.id,
                'text': text,
                'index': 0
            }
            config.users_data.append(data)
    else:
        config.users_data = [{
            'user_id': message.from_user.id,
            'text': text,
            'index': 0
        }]

    if text == '':
        t = 'Запрос не может быть пустым!'
        await message.answer(t)
    else:
        # Выдача ответа пользователю
        yt = YouTubeApi(message.from_user.id)
        video_url, video_id = yt.get_search_url_id(text)

        not_found_user = True
        for item in config.users_data:
            if item['user_id'] == message.from_user.id:
                item['video'] = video_id
                not_found_user = False
        if not_found_user:
            print('User not found!')

        if not video_url:
            await message.answer('Произошла ошибка при поиске! Повтори попытку позже.')

        if video_url:
            new_text = 'Советую глянуть это: ' + str(video_url)
            await message.answer(new_text, reply_markup=get_video_kb())
