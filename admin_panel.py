from aiogram import F
from keyboards import receipt_time_kb
from shop_bot import dp
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest


@dp.callback_query(F.data == 'start_admin')
async def process_callback_confirm_order(callback_query: CallbackQuery):

    try:
        await callback_query.message.answer(
            text='{0}, приветствую Вас в панели администратора\nПожалуйста, воспользуйтесь кнопками'.format(
                callback_query.from_user.first_name),
            reply_markup=receipt_time_kb())
    except TelegramBadRequest:
        await callback_query.answer()


@dp.callback_query(F.data == 'start_adding')
async def process_callback_confirm_order(callback_query: CallbackQuery):

    try:
        await callback_query.message.answer(
            text='{0}, ваш заказ успешно подтверждён\nПожалуйста, укажите через какое время заберете заказ'.format(
                callback_query.from_user.first_name),
            reply_markup=receipt_time_kb())
    except TelegramBadRequest:
        await callback_query.answer()