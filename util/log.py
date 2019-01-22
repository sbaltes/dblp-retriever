""" Global logger. """

import logging


def configure_logger(name, log_file):
    """
    Configure a named global logger.
    (see also [1])
    :param name: Name of global logger.
    :param log_file: Path to log file for FileHandler.
    [1]: http://stackoverflow.com/a/7622029
    """

    logger = logging.getLogger(name)  # name is None => returns root logger

    log_formatter = logging.Formatter(fmt='%(asctime)s %(name)s %(levelname)s: %(message)s')

    # write log messages to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)

    # write log messages to log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
