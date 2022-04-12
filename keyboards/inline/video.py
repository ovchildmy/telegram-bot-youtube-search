from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def get_video_kb():
    kb = InlineKeyboardMarkup()
    btns = [
        {
            'name': 'Нравится',
            'act': 'like'
        },
        {
            'name': 'Следующее',
            'act': 'next'
        }
    ]

    buttons = []
    for btn in btns:
        buttons.append(InlineKeyboardButton(btn['name'], callback_data=btn['act']))
    kb.row(*buttons)

    return kb
