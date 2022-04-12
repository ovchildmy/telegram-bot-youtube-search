import asyncio
import time

import json
import requests
from aiogram import types
from aiogram.types import CallbackQuery
from data import config
from keyboards.inline.video import get_video_kb
from loader import dp
from utils.YouTubeApi import YouTubeApi


@dp.callback_query_handler(lambda x: x.data == 'like')
async def like(callback_query: CallbackQuery):
    """ нажатие кнопки "нравится" """
    yt = YouTubeApi(callback_query.from_user.id, callback_query.message)
    video_id = -1

    for item in config.users_data:
        if item['user_id'] == callback_query.from_user.id:
            video_id = item['video']

        if item['user_id'] == callback_query.from_user.id and 'access_token' in item:
            print('access token exists')
            result = await yt.like_video(video_id)
        else:
            url = 'https://oauth2.googleapis.com/device/code?client_id=46899328355-fjsv0gnfnr702d698iuj3el4t5s5ub3o.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/youtube'
            response = requests.post(url)  # получение данных для верификации пользователя

            if response.ok:
                data = json.loads(response.text)
                print('response data:', data)
                user_code = data['user_code']
                text = f'Чтобы поставить лайк, перейдите по ссылке https://www.google.com/device и введите код '
                text_code = f'<b>{user_code}</b>'
                next_time = time.time()
                end_time = time.time() + data['expires_in']
            else:
                text = 'Произошла непредвиденная ошибка. Повторите попытку позже.'

            response_msg_1 = await callback_query.message.answer(text, parse_mode=types.ParseMode.HTML)
            response_msg_2 = await callback_query.message.answer(text_code, parse_mode=types.ParseMode.HTML)
            await poll_google_request(next_time, end_time, data, data['device_code'], yt, video_id,
                                      callback_query.from_user.id, [response_msg_1, response_msg_2], callback_query)


# Каждые 5 секунд требуется проверять, подтвердил ли пользователь устройство
async def poll_google_request(next_time, end_time, data, device_code, yt, video_id, user_id, response_msg,
                              callback_query):
    while True:
        url = 'https://oauth2.googleapis.com/token'
        p = {
            'client_id': config.CLIENT_ID,
            'client_secret': config.CLIENT_SECRET,
            'device_code': device_code,
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
        }
        response = requests.post(url, params=p)

        if response.ok:  # пользователь подтвердил устройство
            for msg in response_msg:
                await msg.delete()

            await callback_query.message.answer('Устройство подтверждено!')

            # запись токена в бд
            for item in config.users_data:
                if item['user_id'] == user_id:
                    item['access_token'] = json.loads(response.text)['access_token']

            # нужно поставить лайк на предложенное видео
            print('access token dosnt exists')
            result = await yt.like_video(video_id)
            break

        # переподключение
        print('reconnect')
        if next_time >= end_time:
            print('end of conn time')
            break
        next_time += data['interval']
        await asyncio.sleep(data['interval'])


@dp.callback_query_handler(lambda x: x.data == 'next')
async def next(callback_query: CallbackQuery):
    """ нажатие на кнопку "следующее" """
    for item in config.users_data:
        if item['user_id'] == callback_query.from_user.id:
            text = item['text']

            yt = YouTubeApi(callback_query.from_user.id)
            video_url, video_id = yt.get_search_url_id(text)

            item['video'] = video_id
            if not video_url:
                await callback_query.answer('Произошла ошибка при поиске! Повтори попытку позже.')

            if video_url:
                new_text = 'Советую глянуть это: ' + video_url
                await callback_query.message.answer(new_text, reply_markup=get_video_kb())
            else:
                err_text = 'Произошла непредвиденная ошибка. Повторите попытку позднее.'
                await callback_query.message.answer(err_text, reply_markup=get_video_kb())
