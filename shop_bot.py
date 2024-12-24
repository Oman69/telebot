import uuid
from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile

from basket import Basket
from bot_config import BOT_TOKEN
from keyboards import full_menu_kb, start_kb, product_to_menu_kb, product_from_basket_kb, product_to_basket_kb, \
    basket_kb
from db_utils import select_from_table
from create_db import products

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
bs = Basket()

@dp.callback_query(F.data == 'basket')
async def process_callback_basket(callback_query: CallbackQuery):
    basket_text = bs.view_all_basket()
    try:
        await callback_query.message.answer(
            text=basket_text,
            reply_markup=basket_kb()
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


@dp.callback_query(F.data == 'salad')
async def process_callback_product(callback_query: CallbackQuery):
    result = select_from_table(products, params={'value': 'salad'})
    try:
        for product in result.fetchall():
            img = FSInputFile('images/salad.jpeg')
            name = product.t[1]
            weight = product.t[3]
            price = product.t[4]
            caption = name + '\n' + str(weight) + ' грамм\n' + str(price) + ' рублей\nВ корзине: 0'
            product_id = str(product.t[0])
            await callback_query.message.answer_photo(img,
                                                      caption=caption,
                                                      reply_markup=product_to_basket_kb(product_id, 0))
        await callback_query.message.answer(
            text='Вернуться в меню',
            reply_markup=product_to_menu_kb())

    except FileNotFoundError:
        await callback_query.answer()


@dp.callback_query(F.data == 'menu')
async def process_callback_menu(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
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


if __name__ == '__main__':
    dp.run_polling(bot)
