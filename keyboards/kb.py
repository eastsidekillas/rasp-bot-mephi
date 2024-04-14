from aiogram.utils.keyboard import InlineKeyboardBuilder
from functions.getGroup import parse_groups


def start_kb():
    ikb = InlineKeyboardBuilder()
    ikb.button(text='Давай начнём🚀', callback_data='go_start')

    return ikb.as_markup()


def all_groups(groups):
    if not isinstance(groups, dict):
        groups = dict(groups)
    ikb = InlineKeyboardBuilder()
    for group_name, group_value in groups.items():
        ikb.button(text=group_name, callback_data=f'group_btn_{group_value}')
    ikb.adjust(3)

    return ikb.as_markup()



