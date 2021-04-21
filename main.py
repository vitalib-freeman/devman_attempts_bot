import requests
from requests.exceptions import Timeout
import time
import logging

#TODO store securely
TOKEN = '46831f92d5bb3c243ac1fa7ce1d9774d59a6f89c'
SUBMITTED_TASKS_URL = 'https://dvmn.org/api/user_reviews/'
LONG_POLLING_TASKS_URL = 'https://dvmn.org/api/long_polling/'

def getFromDmvnApi(url, token, timestamp, timeout=5):
    headers = {'Authorization': f'Token {TOKEN}'}
    payload = {
        'timestamp': timestamp
    }
    while True:
        try:
            response = requests.get(url, headers=headers, params=payload, timeout=timeout)
            response.raise_for_status()
        except Timeout as e:
            logging.error(e)
            continue
    return response.json()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Debug is enabled")
    # json_response = getFromDmvnApi(SUBMITTED_TASKS_URL, TOKEN)
    # print(json_response)
    timestamp = time.time()
    while True:
        long_polling_response = getFromDmvnApi(LONG_POLLING_TASKS_URL, TOKEN, timestamp)
        if (long_polling_response['status'] == 'found'):
            timestamp = long_polling_response['last_attempt_timestamp']
            logging.debug(long_polling_response)
        else:
            timestamp = long_polling_response['timestamp_to_request']
        logging.debug(timestamp)
