import os
from time import sleep

from bahn import start_downloads
from logging_setup import init_bahn_logger

logger = init_bahn_logger()


SCRIPT_PATH = os.path.join(os.getcwd(), "src/bahn.py")
WAIT = 2
COMMAND = ['python3', SCRIPT_PATH]


def start():
    try:
        start_downloads()
    except Exception as e:
        logger.error(str(e))
        handle_crash()


def handle_crash():
    # Restart the script after short sleep
    sleep(WAIT)
    logger.info('Restarting script now')
    print('Restarting script now...')
    start()


if __name__ == '__main__':
    print('Start script called')
    logger.info('Start script called')
    start()
