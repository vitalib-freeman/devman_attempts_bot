import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, Timeout

DEVMAN_ATTEMPTS_URL = 'https://dvmn.org/api/long_polling/'


def fetch_devman_attempts(url, devman_toeken, timestamp, timeout=90):
    headers = {'Authorization': f'Token {devman_toeken}'}
    payload = {
        'timestamp': timestamp
    }
    while True:
        try:
            response = requests.get(
                url,
                headers=headers,
                params=payload,
                timeout=timeout
            )
            response.raise_for_status()
            break
        except (Timeout, ConnectionError) as e:
            logging.error(e)
            time.sleep(timeout)
            continue
    return response.json()


def convert_message(attempt):
    positive_result = 'Преподатавателю все понравилось, можно приступать \
         к следующему уроку! '
    negative_result = 'К сожалению в работе нашлись ошибки! '
    return "У вас проверили работу <a href='{}'>{}</a>\n\n{}".format(
        "https://dvmn.org{}".format(attempt['lesson_url']),
        attempt['lesson_title'],
        negative_result if attempt['is_negative'] else positive_result,
    )


if __name__ == '__main__':
    load_dotenv()
    devman_api_token = os.getenv('DEVMAN_API_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    timestamp = time.time()
    while True:
        response = fetch_devman_attempts(
            DEVMAN_ATTEMPTS_URL,
            devman_api_token,
            timestamp
        )
        if (response['status'] == 'found'):
            for attempt in response['new_attempts']:
                bot.send_message(
                    telegram_chat_id,
                    text=convert_message(attempt),
                    parse_mode=telegram.ParseMode.HTML
                )
            timestamp = response['last_attempt_timestamp']
        else:
            timestamp = response['timestamp_to_request']
