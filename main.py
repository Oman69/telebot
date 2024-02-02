#@suka_nahuy_bot

from data.auth import bot
import requests
from telebot import types

@bot.message_handler(commands=['start'])
def start(message):
    hello = f'Привет,{message.from_user.first_name}'
    bot.send_message(message.chat.id, hello, parse_mode='html')

# Создание кнопок

@bot.message_handler(commands=['go'])
def start(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_btc = types.KeyboardButton('BTC')
    btn_eth = types.KeyboardButton('ETH')
    btn_ltc = types.KeyboardButton('LTC')
    btn_trx = types.KeyboardButton('TRX')
    btn_xrp = types.KeyboardButton('XRP')
    markup.add(btn_btc, btn_eth,btn_ltc, btn_trx, btn_xrp)
    bot.send_message(message.chat.id, 'Выберите монету',  reply_markup=markup)

# Создание запроса к API

@bot.message_handler()
def start(message):
    btc = requests.get(f'https://yobit.net/api/3/ticker/{message.text.lower()}_usdt')
    response = btc.json()
    mess = f'Цена {message.text.upper()}: {response[f"{message.text.lower()}_usdt"]["sell"]}'
    bot.send_message(message.chat.id, mess,  parse_mode='html')

# Запуск бота
bot.polling(none_stop=True)