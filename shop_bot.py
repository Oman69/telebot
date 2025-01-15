import uuid
from datetime import datetime, timedelta
from create_db import products
from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from basket import Basket
from bot_config import BOT_TOKEN, ADMINS
from keyboards import full_menu_kb, start_kb, product_to_menu_kb, product_from_basket_kb, product_to_basket_kb, \
    basket_kb, receipt_time_kb, admin_start_kb, admin_menu_kb
from db_utils import select_from_table
from product_class import Product

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def send_to_admin(message: str):
    for admin_id in ADMINS:
        await bot.send_message(chat_id=admin_id, text=message, parse_mode='HTML')


@dp.callback_query(F.data.split(':')[0] == 'receipt_time')
async def process_callback_from_basket(callback_query: CallbackQuery):
    time_now = datetime.now()
    minutes = callback_query.data.split(':')[1]
    receipt_time = time_now + timedelta(minutes=int(minutes))
    # Сохранить время получения в БД
    bs.save_ordered_time(receipt_time)
    order_number = bs.get_order_number()
    # ToDo Отправить сообщение администратору о заказе
    # Создать сообщение для админа
    message = bs.create_message_about_new_order(order_number, receipt_time)
    await send_to_admin(message)
    try:
        await callback_query.message.answer(
            text='Заказ оформлен и будет готов к получению через ' + minutes + ' минут.\nНомер заказа - ' + str(
                order_number),
            reply_markup=product_to_menu_kb(), parse_mode='HTML'
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'confirm_order')
async def process_callback_confirm_order(callback_query: CallbackQuery):
    bs.confirm_order()
    try:
        await callback_query.message.answer(
            text='{0}, ваш заказ успешно подтверждён\nПожалуйста, укажите через какое время заберете заказ'.format(
                callback_query.from_user.first_name),
            reply_markup=receipt_time_kb())
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'delete_order')
async def process_callback_delete_order(callback_query: CallbackQuery):
    bs.delete_order()
    try:
        await callback_query.message.answer(
            text='Ваш заказ успешно отменен',
            reply_markup=start_kb(callback_query.from_user.id)),
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'basket')
async def process_callback_basket(callback_query: CallbackQuery):
    basket_text = bs.view_all_basket()
    if basket_text != 'Товары в корзину не добавлены\n':
        keyboard = basket_kb()
    else:
        keyboard = start_kb(callback_query.from_user.id)
    try:
        await callback_query.message.answer(
            text=basket_text,
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data.split(':')[0] == 'to_basket')
async def process_callback_to_basket(callback_query: CallbackQuery):
    try:
        product_id = uuid.UUID(callback_query.data.split(':')[1])
        user_id = callback_query.from_user.id
        # Посмотреть количество записей в orders_products
        row, current_value = bs.check_product_in_order(product_id)

        if row != 0:
            bs.change_value_in_basket(product_id, current_value)
        else:
            bs.insert_product_to_table(user_id, product_id)

        await callback_query.message.edit_caption(
            caption=callback_query.message.caption.split(':')[0] + ': ' + str(current_value + 1),
            reply_markup=product_from_basket_kb(str(product_id)), parse_mode='HTML'
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data.split(':')[0] == 'from_basket')
async def process_callback_from_basket(callback_query: CallbackQuery):
    product_id = uuid.UUID(callback_query.data.split(':')[1])
    current_value = bs.get_current_value_by_product_id(product_id)
    bs.change_value_in_basket(product_id, current_value, False)
    new_value = current_value - 1
    try:
        await callback_query.message.edit_caption(
            caption=callback_query.message.caption.split(':')[0] + ': ' + str(new_value),
            reply_markup=product_to_basket_kb(str(product_id), new_value), parse_mode='HTML'
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data.split(':')[0] == 'category')
async def process_callback_product(callback_query: CallbackQuery):
    category = callback_query.data.split(':')[1]
    result = select_from_table(products, params={'value': category})
    try:
        for product in result.fetchall():
            img = FSInputFile('images/salad.jpeg')
            product_id, name, description, weight, price, category = product.t
            current_value = bs.get_current_value_by_product_id(product_id)
            caption = name + '\n' + str(weight) + ' грамм\n' + str(price) + ' рублей\nВ корзине: ' + str(current_value)
            await callback_query.message.answer_photo(img,
                                                      caption=caption,
                                                      reply_markup=product_to_basket_kb(str(product_id), current_value))
        await callback_query.message.answer(
            text='Вернуться в меню',
            reply_markup=product_to_menu_kb())

    except FileNotFoundError:
        await callback_query.answer()


@dp.callback_query(F.data == 'menu')
async def process_callback_menu(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text='Выберите категорию, чтобы вывести список товаров:',
        reply_markup=full_menu_kb()
    )


@dp.callback_query(F.data == 'start_buttons')
async def start_message(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text='{0.first_name}, выберите все самое вкусное в нашем меню 🍽 \nили проверьте покупки в корзине 🛒'.format(
            callback_query.from_user),
        reply_markup=start_kb(callback_query.from_user.id))


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    global bs
    bs = Basket()
    await message.answer(text="Привет, {0.first_name} 👋\nВоспользуйся кнопками".format(message.from_user),
                         reply_markup=start_kb(message.from_user.id))


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения
@dp.message()
async def send_echo(message: Message):
    try:
        await message.answer(
            text="Привет, {0.first_name} 👋\nЯ не поддерживаю эти ваши GPT, поэтому воспользуйся кнопками".format(
                message.from_user),
            reply_markup=start_kb(message.from_user.id))
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy')


# Admin callbacks
@dp.callback_query(F.data == 'start_admin')
async def start_admin(callback_query: CallbackQuery):

    try:
        await callback_query.message.answer(
            text='{0}, приветствую Вас в панели администратора\nПожалуйста, выберите требуемое действие'.format(
                callback_query.from_user.first_name),
            reply_markup=admin_start_kb())
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'add_new_product')
async def add_new_product(callback_query: CallbackQuery):

    try:
        await callback_query.message.answer(
            text='Выберите категорию для нового товара',
            reply_markup=admin_menu_kb())
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data.split(':')[0] == 'cat')
async def get_category(callback_query: CallbackQuery):
    category = callback_query.data.split(':')[1]
    pr = Product()
    pr.product_data['category'] = category
    try:
        await callback_query.message.answer(
            text='Введите наименование товара в формате: \nname:Наименование)',
            reply_markup=admin_menu_kb())
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data.split(':')[0] == 'name')
async def get_category(callback_query: CallbackQuery):
    name = callback_query.data.split(':')[1]
    pr.product_data['category'] = name
    try:
        await callback_query.message.answer(
            text='Введите данные о новом товаре в формате: \nname:Наименование)',
            reply_markup=admin_menu_kb())
    except TelegramBadRequest:
        await callback_query.answer()


if __name__ == '__main__':
    dp.run_polling(bot)
