from aiogram import Dispatcher

from .is_admin import AdminFilter
from . import video


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
