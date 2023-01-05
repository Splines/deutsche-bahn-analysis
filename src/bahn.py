import os
import time
import zlib
from datetime import datetime
from typing import Tuple

import pytz
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
STATION_NUMBER = '8005628'  # Speyer
HEADERS = {
    'DB-Client-Id': os.getenv('CLIENT_ID'),
    'DB-Api-Key': os.getenv('CLIENT_KEY')
}


def make_request_and_save(full_request=False):
    # Check for full hour when we make a full request
    # (instead of only querying recent changes)
    global elapsed_time
    elapsed_time += INTERVAL_SECONDS
    is_hourly = False
    if elapsed_time == HOUR_IN_SECONDS:
        elapsed_time = 0
        is_hourly = True
    if full_request:
        is_hourly = True

    # API call: planned data
    if is_hourly:
        url = _construct_url_for_planned_stations()
        logger.info(f"Calling endpoint: plan/{STATION_NUMBER}")
        is_error, xml_string = _make_api_call(url)
        if not is_error:
            _compress_and_save(xml_string, 'plan')

    # API call: changes in data
    path_suffix = 'full' if is_hourly else 'recent'
    url_switch = 'f' if is_hourly else 'r'
    url = BASE_URL + f'timetables/v1/{url_switch}chg/{STATION_NUMBER}'
    logger.info(f"Calling endpoint: {url_switch}chg/{STATION_NUMBER}")
    is_error, xml_string = _make_api_call(url)
    if not is_error:
        _compress_and_save(xml_string, path_suffix)


def _construct_url_for_planned_stations():
    now = datetime.now(tz=pytz.timezone('Europe/Berlin'))
    date = now.strftime("%y%m%d")
    hour = now.strftime("%H")
    url = BASE_URL + f'timetables/v1/plan/{STATION_NUMBER}/{date}/{hour}'
    return url


def _make_api_call(url) -> Tuple[bool, str]:
    xml_string = ""
    api_error = False
    try:
        r = requests.get(url, headers=HEADERS)
        xml_string = r.text
    except Exception as e:
        logger.error(f'Could not GET: {url}')
        logger.error(str(e))
        api_error = True
    return api_error, xml_string


def _compress_and_save(string, path_suffix):
    # Remove empty lines
    string = os.linesep.join([s for s in string.splitlines() if s])
    # Compress
    bytes = zlib.compress(string.encode('utf-8'),
                          level=zlib.Z_BEST_COMPRESSION)
    # Save response
    datetime_string = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = f'./download/{time.time()}-{datetime_string}-{path_suffix}.xml.compressed'
    with open(path, 'wb') as f:
        f.write(bytes)


def _check_for_downloads_directory():
    if not os.path.exists('./download'):
        os.mkdir('./download/')


def start_downloads():
    _check_for_downloads_directory()

    print('Waiting till next minute...')
    # sleep_till_start_of_next_minute()
    print('Started bahn.py execution...')
    # one full request in the beginning
    make_request_and_save(full_request=True)
    every(INTERVAL_SECONDS, make_request_and_save, execute_immediately=False)
