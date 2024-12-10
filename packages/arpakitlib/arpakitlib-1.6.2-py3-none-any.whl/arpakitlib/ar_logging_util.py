# arpakit

import logging
import os
from typing import Optional

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def init_log_file(*, log_filepath: str):
    if not os.path.exists(path=log_filepath):
        with open(file=log_filepath, mode="w") as file:
            file.write("")


_normal_logging_was_setup: bool = False


def setup_normal_logging(log_filepath: Optional[str] = None):
    global _normal_logging_was_setup
    if _normal_logging_was_setup is True:
        return

    if log_filepath:
        init_log_file(log_filepath=log_filepath)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s - %(message)s",
        datefmt="%d.%m.%Y %I:%M:%S%p"
    )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    if log_filepath:
        file_handler = logging.FileHandler(log_filepath)
        file_handler.setLevel(logging.WARNING)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d - %(message)s",
            datefmt="%d.%m.%Y %I:%M:%S%p"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    _normal_logging_was_setup = True

    logger.info("normal logging was setup")


def __example():
    pass


if __name__ == '__main__':
    __example()
