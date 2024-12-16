from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from bot_config import BOT_TOKEN

# Создаем объекты бота и диспетчера
from keyboards import product_menu_kb, full_menu_kb, start_kb, product_to_menu_kb

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


@dp.callback_query(F.data == 'salad')
async def process_callback_product(callback_query: CallbackQuery):
    products = [{'img': FSInputFile('images/salad.jpeg'), 'caption': 'Салат греческий\nВес: 150 гр\nЦена: 200 руб','id': 1, 'in_basket': 0},
                {'img': FSInputFile('images/salad.jpeg'), 'caption': 'Салат японский\nВес: 160 гр\nЦена: 230 руб','id': 2, 'in_basket': 0}]
    try:
        for product in products:
            await callback_query.message.answer_photo(product['img'],
                                                      caption=product['caption'],
                                                      reply_markup=product_menu_kb())
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
        text='{0.first_name}, выберите все самое вкусное в нашем меню 🍽 \nили проверьте покупки в корзине 🛒'.format(callback_query.from_user),
        reply_markup=start_kb(callback_query.from_user.id))


#Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text="Привет, {0.first_name} 👋\nВоспользуйся кнопками".format(message.from_user),
                         reply_markup=start_kb(message.from_user.id))


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy')

if __name__ == '__main__':
    dp.run_polling(bot)