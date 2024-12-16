from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot_config import ADMINS


def start_kb(user_telegram_id: int):
    kb_list = [[InlineKeyboardButton(text="🛒 Корзина", callback_data='basket'),
                InlineKeyboardButton(text="🍽 Меню", callback_data='menu')]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                       resize_keyboard=True,
                                       one_time_keyboard=True,
                                       input_field_placeholder="Воспользуйтесь меню:")
    if user_telegram_id in ADMINS:
        kb_list.append([InlineKeyboardButton(text="⚙️Админ панель")])
    return keyboard


def full_menu_kb():
    kb_list = [[InlineKeyboardButton(text="🍲 Супы", callback_data='soup'),
                InlineKeyboardButton(text="🍛 Гарниры", callback_data='garnish')],
               [InlineKeyboardButton(text="🍝 Вторые блюда", callback_data='cutlet'),
                InlineKeyboardButton(text="🥗 Салаты", callback_data='salad')],
               [InlineKeyboardButton(text="🎂 Десерты", callback_data='cutlet'),
                InlineKeyboardButton(text="☕ Напитки", callback_data='salad')],
               [InlineKeyboardButton(text="↩ Назад", callback_data='start_buttons')]
               ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                       resize_keyboard=True,
                                       one_time_keyboard=True,
                                       input_field_placeholder="Воспользуйтесь меню:")
    return keyboard


def product_menu_kb():
    kb_list = [[InlineKeyboardButton(text="✅ Добавить в корзину", callback_data='to_basket')]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                       resize_keyboard=True,
                                       one_time_keyboard=True)
    return keyboard


def product_to_menu_kb():
    kb_list = [[InlineKeyboardButton(text="↩ Назад", callback_data='menu')],
               [InlineKeyboardButton(text="🛒 Корзина", callback_data='basket')]]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                       resize_keyboard=True,
                                       one_time_keyboard=True)
    return keyboard