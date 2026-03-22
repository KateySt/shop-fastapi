import logging

from logtail import LogtailHandler

from app.config import log_config


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logtail_handler = LogtailHandler(
        source_token=log_config.BETTER_STACK_TOKEN,
        host=log_config.BETTER_STACK_URL,
    )
    logtail_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(logtail_handler)
    logger.addHandler(console_handler)

    return logger
