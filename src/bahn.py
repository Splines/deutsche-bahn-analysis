import os
import zlib
from datetime import datetime

import requests
from dotenv import load_dotenv

from logging_setup import get_bahn_logger
from schedule import every, sleep_till_start_of_next_minute

load_dotenv()

logger = get_bahn_logger()

# has to add up to one hour, otherwise script will break (!)
INTERVAL_SECONDS = 60 * 5  # every 5 minutes
HOUR_IN_SECONDS = 60 * 60
elapsed_time = 0

BASE_URL = 'https://apis.deutschebahn.com/db-api-marketplace/apis/'

station_eva_number = '8005628'  # Speyer
# date = '230103'  # 3. Januar 2023
# hour = '18'  # 9 Uhr
# url = 'https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/'\
#      + f'/{station_eva_number}/{date}/{hour}'
# url = 'https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/rchg/'\
#     + f'{station_eva_number}'

headers = {
    'DB-Client-Id': os.getenv('CLIENT_ID'),
    'DB-Api-Key': os.getenv('CLIENT_KEY')
}


def make_request_and_save(full_request=False):
    global elapsed_time
    elapsed_time += INTERVAL_SECONDS
    is_hourly = False
    if elapsed_time == HOUR_IN_SECONDS:
        elapsed_time = 0
        is_hourly = True
    if full_request:
        is_hourly = True

    path_suffix = 'full' if is_hourly else 'recent'

    # API call
    url_switch = 'f' if is_hourly else 'r'
    url = BASE_URL + f'timetables/v1/{url_switch}chg/{station_eva_number}'
    logger.info(f"Calling endpoint: {url_switch}chg/{station_eva_number}")

    xml_string = ""
    api_error = False
    try:
        r = requests.get(url, headers=headers)
        xml_string = r.text
    except Exception as e:
        logger.error(f'Could not GET url {url}')
        logger.error(str(e))
        api_error = True

    # TODO: if is_hourly -> also make API call to "planned" endpoint

    if not api_error:
        # Compress
        bytes = zlib.compress(xml_string.encode('utf-8'),
                              level=zlib.Z_BEST_COMPRESSION)
        # Save response
        filename = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        path = f'./download/{filename}-{path_suffix}.xml.compressed'
        with open(path, 'wb') as f:
            f.write(bytes)


def _check_for_downloads_directory():
    if not os.path.exists('./download'):
        os.mkdir('./download/')


def start_downloads():
    _check_for_downloads_directory()

    # print('Waiting till next minute...')
    # sleep_till_start_of_next_minute()
    print('Started bahn.py execution...')
    # one full request in the beginning
    make_request_and_save(full_request=True)
    every(INTERVAL_SECONDS, make_request_and_save, execute_immediately=False)
