import logging
from typing import NoReturn

import sentry_sdk
from fastapi import HTTPException, status
from sentry_sdk import capture_message
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.config import app_config, get_logger, sentry_config

logger = get_logger(__name__)


def unexpected_error(
    log_message: str, user_message: str = "General error. Call support"
) -> NoReturn:
    logger.error(log_message)
    capture_message(log_message, level="error")
    raise HTTPException(detail=user_message, status_code=status.HTTP_400_BAD_REQUEST)


def init_sentry():
    sentry_sdk.init(
        dsn=sentry_config.SENTRY_DNS,
        environment=app_config.APP_ENV,
        send_default_pii=True,
        traces_sample_rate=1.0,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
    )
