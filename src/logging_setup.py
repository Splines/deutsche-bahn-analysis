import logging
import logging.handlers
import os


def disable_logger():
    logging.disable(logging.CRITICAL)


def init_wrapper_logger():
    logger = logging.getLogger('wrapper')
    logger.setLevel(logging.DEBUG)

    # File handler
    _check_for_log_directory()
    logger.addHandler(_get_roll_over_handler('./logs/wrapper.log'))

    print('Wrapper logger initiated')
    return logger


def init_bahn_logger():
    logger = logging.getLogger('bahn')
    logger.setLevel(logging.DEBUG)

    # File handler
    _check_for_log_directory()
    logger.addHandler(_get_roll_over_handler('./logs/bahn.log'))

    print('Deutsche Bahn logger initiated')
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
        "%(asctime)s;%(levelname)s;%(name)s;%(message)s", "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)

    return log_handler


if __name__ == '__main__':
    print('Setting up logger...')
    # write to stderr
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(console_handler)
