
from logging import handlers
import logging
import sys

def get_formater():
    return logging.Formatter(
        "[%(name)-10s-%(levelname)-5s %(asctime)s] %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

def get_logger(name, filename=None, debug=False, noprint=False):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    formater = get_formater()

    if not noprint:
        add_stdout_handler(logger)

    if filename:
        try:
            file_stream_handler = logging.handlers.RotatingFileHandler(
                filename, maxBytes=10_000_000
            )
            file_stream_handler.setFormatter(formater)
            logger.addHandler(file_stream_handler)
        except AttributeError as e:
            pass
    return logger

def add_stdout_handler(logger):
    formater = get_formater()
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formater)
    logger.addHandler(stream_handler)