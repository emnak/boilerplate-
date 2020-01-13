import logging
import sys

FORMATTER = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(filename)s  %(funcName)s::line %(lineno)d: %(message)s"
)


def get_logger(name="unknown_logger"):
    """
    Creates a logger with the DEBUG level of information.
    Args:
        name (str): name of the logger

    Returns:
        logger: a Logger object
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(FORMATTER)
    logger.addHandler(handler)
    logger.propagate = False  # to avoid printing the same logs multiple times
    return logger
