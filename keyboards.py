from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_config import ADMINS


def start_kb(user_telegram_id: int):
    kb_list = [[InlineKeyboardButton(text="🛒 Корзина", callback_data='basket'),
                InlineKeyboardButton(text="🍽 Меню", callback_data='menu')]]

    if user_telegram_id in ADMINS:
        kb_list.append([InlineKeyboardButton(text="⚙️Админ панель", callback_data='start_admin')])

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                    resize_keyboard=True,
                                    one_time_keyboard=True,
                                    input_field_placeholder="Воспользуйтесь меню:")
    return keyboard


def full_menu_kb():
    kb_list = [[InlineKeyboardButton(text="🍲 Супы", callback_data='category:soup'),
                InlineKeyboardButton(text="🍛 Гарниры", callback_data='category:garnish')],
               [InlineKeyboardButton(text="🍝 Вторые блюда", callback_data='category:cutlet'),
                InlineKeyboardButton(text="🥗 Салаты", callback_data='category:salad')],
               [InlineKeyboardButton(text="🎂 Десерты", callback_data='category:cutlet'),
                InlineKeyboardButton(text="☕ Напитки", callback_data='category:drinks')],
               [InlineKeyboardButton(text="↩ Назад", callback_data='start_buttons')]
               ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                    resize_keyboard=True,
                                    one_time_keyboard=True,
                                    input_field_placeholder="Воспользуйтесь меню:")
    return keyboard


def admin_menu_kb():
    kb_list = [[InlineKeyboardButton(text="🍲 Супы", callback_data='cat:soup'),
                InlineKeyboardButton(text="🍛 Гарниры", callback_data='cat:garnish')],
               [InlineKeyboardButton(text="🍝 Вторые блюда", callback_data='cat:cutlet'),
                InlineKeyboardButton(text="🥗 Салаты", callback_data='cat:salad')],
               [InlineKeyboardButton(text="🎂 Десерты", callback_data='cat:cutlet'),
                InlineKeyboardButton(text="☕ Напитки", callback_data='cat:drinks')],
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


def admin_start_kb():
    kb_list = [
        [InlineKeyboardButton(text="Добавить новый товар", callback_data='add_new_product')],
        [InlineKeyboardButton(text="Посмотреть текущие заказы", callback_data='get_orders_by_day')],
        [InlineKeyboardButton(text="Удалить товар", callback_data='delete_product')],
        [InlineKeyboardButton(text="Удалить все заказы", callback_data='delete_all_orders')],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb_list,
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
    return keyboard