from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from bot_config import BOT_TOKEN
from keyboards import full_menu_kb, start_kb, product_to_menu_kb, product_from_basket_kb, product_to_basket_kb
from db.db_utils import insert_to_table, select_from_table
from db.create_db import products

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.callback_query(F.data == 'basket')
async def process_callback_basket(callback_query: CallbackQuery):
    try:
        await callback_query.message.edit_text(
            text='Была нажата КОРЗИНА',
            reply_markup=callback_query.message.reply_markup
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'to_basket')
async def process_callback_to_basket(callback_query: CallbackQuery):
    # ToDo Добавить в БД
    try:
        await callback_query.message.edit_caption(
            caption=callback_query.message.caption + '\n' + '<b>✔️Товар добавлен в корзину</b>',
            reply_markup=product_from_basket_kb(), parse_mode='HTML'
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'from_basket')
async def process_callback_to_basket(callback_query: CallbackQuery):
    # ToDo Удалить из БД
    try:
        await callback_query.message.edit_caption(
            caption=callback_query.message.caption + '\n' + '<b>❗ Товар удален из корзины</b>',
            reply_markup=product_to_basket_kb(), parse_mode='HTML'
        )
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'salad')
async def process_callback_product(callback_query: CallbackQuery):
    result = select_from_table(products, {'value': 'salad'})
    try:
        for product in result:
            print(product)
            img = FSInputFile('images/salad.jpeg')
            name = product._data[1]
            weight = product._data[3]
            price = product._data[4]
            caption = name + '\n' + str(weight) + ' грамм\n' + str(price) + ' рублей\n'
            await callback_query.message.answer_photo(img,
                                                      caption=caption,
                                                      reply_markup=product_to_basket_kb())
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


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
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
