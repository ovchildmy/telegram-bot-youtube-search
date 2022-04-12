import asyncio, logging, types
from aiogram import Bot, Dispatcher, executor, types
from utils.notify_admins import on_startup_notify
import middlewares, filters, handlers, keyboards
from utils.set_bot_commands import set_default_commands
from data import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loader import *
# from data import db


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    middlewares.setup(dp)
    filters.setup(dp)
    handlers.errors.setup(dp)
    # handlers.user.setup(dp)

if __name__ == '__main__':
    try:
        print('Bot started work!')
        print('db now:', config.users_data)
        logging.basicConfig(level=logging.INFO)
        executor.start_polling(dp, on_startup=on_startup)

    except Exception as err:
        print(err)