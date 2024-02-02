import time

import requests

API_URL = 'https://api.telegram.org/bot'
BOT_TOKEN = '5757241884:AAHG9G1J5mNovize10fT2rhuJLY2ICM0cx4'

TEXT = 'Новое сообщение!'

MAX_COUNTER = 100

offset: int = -2
counter: int = 0
chat_id: int

while counter < MAX_COUNTER:
    print('attempt =', counter)

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&text={TEXT}')

    time.sleep(1)
    counter += 1