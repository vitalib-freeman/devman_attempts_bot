import logging
import time

import requests
import telegram
from requests.exceptions import ConnectionError, Timeout

#TODO store securely
TOKEN = '46831f92d5bb3c243ac1fa7ce1d9774d59a6f89c'
TELEGRAM_TOKEN = '1756378228:AAHnmYX-KGz5PkEdgz-1hHXhunEp3M7948I'
SUBMITTED_TASKS_URL = 'https://dvmn.org/api/user_reviews/'
LONG_POLLING_TASKS_URL = 'https://dvmn.org/api/long_polling/'
TELEGRAM_RESULT_MESSAGE = "У вас проверили работу {}\n{}"

def getFromDmvnApi(url, token, timestamp, timeout=90):
    headers = {'Authorization': f'Token {TOKEN}'}
    payload = {
        'timestamp': timestamp
    }
    while True:
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=timeout)
            response.raise_for_status()
            break
        except (Timeout, ConnectionError) as e:
            logging.error(e)
            time.sleep(timeout)
            continue
    return response.json()

def convert(attempt):
    positive_result = 'Преподатавателю все понравилось, можно приступать к следующему уроку! '
    negative_result = 'К сожалению в работе нашлись ошибки! '
    return "У вас проверили работу <a href='{}'>{}</a>\n\n{}".format(
        "https://dvmn.org{}".format(attempt['lesson_url']),
        attempt['lesson_title'], 
        negative_result if attempt['is_negative'] else positive_result,
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logging.info(bot.get_me())
    timestamp = time.time()
    chat_id = 1109991497 #TODO fetch from settings
    while True:
        response = getFromDmvnApi(LONG_POLLING_TASKS_URL, TOKEN, timestamp)
        logging.info(response)
        if (response['status'] == 'found'):
            for attempt in response['new_attempts']:
                bot.send_message(chat_id, text=convert(attempt), parse_mode=telegram.ParseMode.HTML)
            timestamp = response['last_attempt_timestamp']
        else:
            timestamp = response['timestamp_to_request']
        logging.debug(timestamp)
