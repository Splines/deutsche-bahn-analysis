import socket
import time
import traceback
from datetime import datetime

# https://stackoverflow.com/a/59548973
socket.setdefaulttimeout(30)  # in seconds

def every(delay: int, task, *args, **kwargs):
    """
    Executes the task with the passed in arguments every `delay` seconds.
    Adapted from https://stackoverflow.com/a/49801719
    """
    next_time = time.time()  # execute immediately
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task(*args, **kwargs)
        except:
            traceback.print_exc()

        # Skip tasks if we are behind schedule
        num_skipped_tasks = (time.time() - next_time) // delay
        next_time += num_skipped_tasks * delay

        next_time += delay

def sleep_till_start_of_next_minute():
    sleeptime = 60 - datetime.utcnow().second
    time.sleep(sleeptime)
