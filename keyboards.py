from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

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


def product_to_basket_kb(product_id: str, product_value: int):
    if product_value == 0:
        kb_list = [[InlineKeyboardButton(text="✅ Добавить в корзину",
                                         callback_data='to_basket' + ':' + product_id)]]
    else:
        kb_list = [[InlineKeyboardButton(text="❌ Удалить из корзины", callback_data='from_basket:' + product_id)],
                   [InlineKeyboardButton(text="✅ Добавить в корзину",
                                         callback_data='to_basket' + ':' + product_id)]]


    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return keyboard


def product_from_basket_kb(product_id: str):
    kb_list = [[InlineKeyboardButton(text="❌ Удалить из корзины", callback_data='from_basket:' + product_id)],
               [InlineKeyboardButton(text="✅ Купить ещё", callback_data='to_basket:' + product_id)]]

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


def basket_kb():
    kb_list = [
                [InlineKeyboardButton(text="🍽 Продолжить покупки", callback_data='menu')],
                [InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data='confirm_order')],
                [InlineKeyboardButton(text="❌ Отменить заказ", callback_data='delete_order')],
               ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return keyboard


def receipt_time_kb():
    kb_list = [
                [InlineKeyboardButton(text="Через 15 минут", callback_data='receipt_time:15')],
                [InlineKeyboardButton(text="Через 30 минут", callback_data='receipt_time:30')],
                [InlineKeyboardButton(text="Через 45 минут", callback_data='receipt_time:45')],
                [InlineKeyboardButton(text="Через 1 час", callback_data='receipt_time:60')],
               ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return keyboard
