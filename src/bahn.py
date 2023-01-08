import os
import time
import zlib
from datetime import datetime

import pytz
import requests
from dotenv import load_dotenv

from logging_setup import get_bahn_logger
from schedule import every, sleep_till_start_of_next_minute
from util.fileutil import create_folder_if_not_exists

load_dotenv()

logger = get_bahn_logger()
DOWNLOAD_FOLDER = './download/'

# has to add up to one hour, otherwise script will break (!)
INTERVAL_SECONDS = 60 * 5  # every 5 minutes
HOUR_IN_SECONDS = 60 * 60
elapsed_time = 0

BASE_URL = 'https://apis.deutschebahn.com/db-api-marketplace/apis/'
HEADERS = {
    'DB-Client-Id': os.getenv('CLIENT_ID'),
    'DB-Api-Key': os.getenv('CLIENT_KEY')
}


def make_request_and_save(stations: list[str], full_request=False):
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

    for station in stations:
        _make_station_request(station, is_hourly)


def _make_station_request(station, is_hourly: bool):
    # API call: planned data
    if is_hourly:
        url = _construct_url_for_planned_stations(station)
        logger.info(f"Calling endpoint: plan/{station}")
        is_error, xml_string = _make_api_call(url)
        if not is_error:
            _compress_and_save(xml_string, station, 'plan')

    # API call: changes in data
    path_suffix = 'full' if is_hourly else 'recent'
    url_switch = 'f' if is_hourly else 'r'
    url = BASE_URL + f'timetables/v1/{url_switch}chg/{station}'
    logger.info(f"Calling endpoint: {url_switch}chg/{station}")
    is_error, xml_string = _make_api_call(url)
    if not is_error:
        _compress_and_save(xml_string, station, path_suffix)


def _construct_url_for_planned_stations(station: str) -> str:
    now = datetime.now(tz=pytz.timezone('Europe/Berlin'))
    date = now.strftime("%y%m%d")
    hour = now.strftime("%H")
    url = BASE_URL + f'timetables/v1/plan/{station}/{date}/{hour}'
    return url


def _make_api_call(url) -> tuple[bool, str]:
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


def _compress_and_save(string: str, station: str, path_suffix: str):
    # Remove all line breaks & empty lines
    # and whitespaces in the beginning and at the end of every line
    string = ''.join([s.strip() for s in string.splitlines() if s])
    # Compress
    bytes = zlib.compress(string.encode('utf-8'),
                          level=zlib.Z_BEST_COMPRESSION)
    # Save response
    datetime_string = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    path = os.path.join(DOWNLOAD_FOLDER, station,
                        f'{time.time()}-{datetime_string}-{station}-{path_suffix}.xml.compressed')
    with open(path, 'wb') as f:
        f.write(bytes)


def _read_stations() -> set[str]:
    stations = []

    with open('./stations.txt', 'r') as f:
        lines = f.readlines()
    for line in lines:
        station = line.split()[0]
        stations.append(station)

    # Avoid duplicates
    stations_set = set(stations)
    if (len(stations) != len(stations_set)):
        logger.info(
            f'Removed {len(stations) - len(stations_set)} duplicate station entrie(s)')

    return stations_set


def start_downloads():
    create_folder_if_not_exists(DOWNLOAD_FOLDER)

    stations = _read_stations()
    logger.info(f'Station eva numbers are: {stations}')
    # Check station folders
    logger.info('Validate station folders')
    for station in stations:
        path = os.path.join(DOWNLOAD_FOLDER, station)
        create_folder_if_not_exists(path)

    print("Waiting 'till next minute...")
    sleep_till_start_of_next_minute()

    print('Started bahn.py execution...')
    logger.info('Started bahn.py execution')
    # one full request in the beginning
    make_request_and_save(stations, full_request=True)
    every(INTERVAL_SECONDS, make_request_and_save,
          False, stations, full_request=False)
