import logging
import logging.handlers
import os

# def disable_logger():
#     logging.disable(logging.CRITICAL)
# dislabe_logger()


def init_bahn_logger():
    logger = logging.getLogger('bahn')
    logger.setLevel(logging.DEBUG)

    # File handler
    _check_for_log_directory()
    logger.addHandler(_get_roll_over_handler('./logs/bahn.log'))

    print('Deutsche Bahn logger initialized')
    return logger


def _check_for_log_directory():
    if not os.path.exists('./logs'):
        os.mkdir('./logs/')


def _get_roll_over_handler(log_filename):
    should_roll_over = os.path.isfile(log_filename)
    log_handler = logging.handlers.RotatingFileHandler(
        log_filename, mode='w', backupCount=10, encoding='utf-8', delay=True)
    if should_roll_over:
        log_handler.doRollover()
    log_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s;%(levelname)s;%(filename)s;%(lineno)d;%(message)s", "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)

    return log_handler


def get_bahn_logger():
    return logging.getLogger('bahn')


if __name__ == '__main__':
    print('Setting up logger...')
    # write to stderr
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(console_handler)
