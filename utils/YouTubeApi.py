import json

from data import config
import requests


class YouTubeApi():
    """
    Класс для работы с YouTubeAPI

    Атрибуты:
    -----------------------
    key : str
        Ключ от Youtube Console
    user_id : int
        id пользователя telegram
    message : aigoram.types.Message
        сообщение пользователя для ответа на него

    Методы
    -----------------------
    get_video_index()
        возвращает индекс видео среди поисковой выдачи Ютуб

    get_search_url_id(text) -> url, id
        принимает поисковое слово
        возвращает url на видео и его id

    like_video(video_id)
        принимает id видео
        ставит лайк ролику
    """
    def __init__(self, user_id, message=None):
        self.key = config.YT_KEY
        self.user_id = user_id
        self.max_results = 10
        self.message = message

    def get_video_index(self):
        if len(config.users_data) > 0:
            item_found = False
            for item in config.users_data:
                if int(item['user_id']) == int(self.user_id):
                    item_found = True
                    index = item['index']
                    if index is None:
                        index = 0

                    if index >= 9:
                        item['index'] = 0
                    else:
                        item['index'] += 1
                    return index

            if not item_found:  # если пользователь не найден в бд
                print('user not found!')
                return 0
        else:
            return 0

    def get_search_url_id(self, text) -> tuple:
        """ Поиск видео по введённым словам """
        if text == '':
            print('Text is empty')
            return None, None

        key = self.key
        # Создание URL`а для выборки видео и взятие данных через API
        url = f'https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&q={text}&key={key}&maxResults=' \
              f'{self.max_results}'
        print(url)
        response = requests.get(url)

        if not response.ok:
            print('response error')
            return response.status_code, None

        index = self.get_video_index()
        print('index is:', index)
        data_json = json.loads(response.text)['items']

        if len(data_json) <= index:
            print('response data is empty:', data_json)
            return False, None

        data = data_json[index]
        print(data)
        video_key = data['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_key}'

        return video_url, video_key

    async def like_video(self, video_id):
        print('like video:', video_id)
        access_token = -1
        for item in config.users_data:
            if item['user_id'] == self.user_id:
                if 'access_token' in item:
                    access_token = item['access_token']
                else:
                    print('access_token not in item')

        url = 'https://www.googleapis.com/youtube/v3/videos/rate'
        p = {
            'access_token': access_token,
            'id': video_id,
            'rating': 'like'
        }

        assert access_token != -1, 'error access_token'

        response = requests.post(url, params=p)
        print(response)
        if response.ok:
            await self.message.answer('Лайк успешно поставлен!')

        return response.ok  # возвращаем результат запроса (прошёл он или нет)
