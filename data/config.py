from environs import Env


env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
ADMINS = env.str('ADMINS')
YT_KEY = env.str('YT_KEY')
CLIENT_ID = env.str('CLIENT_ID')
CLIENT_SECRET = env.str('CLIENT_SECRET')

users_data = []  # объект для хранения последних поисковых запросов пользователей
