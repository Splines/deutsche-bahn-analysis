# adopted from https://stackoverflow.com/a/63021289/
import os
import subprocess
from subprocess import PIPE
from time import sleep

SCRIPT_PATH = os.path.join(os.getcwd(), "src/bahn.py")
WAIT = 2
COMMAND = ['python3', SCRIPT_PATH]


def start():
    try:
        p = subprocess.Popen(COMMAND, stderr=PIPE)
        _, error = p.communicate()
        if p.returncode != 0:
            print('Process error')
            msg = str(error, 'utf-8')
            # logger.error(f'Return code: {p.returncode},\nERROR: {msg}')
            handle_crash()
    except Exception as e:
        print('Some unknown error occurred')
        # logger.error(str(e))
        handle_crash()


def handle_crash():
    # Restart the script after short sleep
    sleep(WAIT)
    print('Restarting script now...')
    start()


print('Start script called')
start()