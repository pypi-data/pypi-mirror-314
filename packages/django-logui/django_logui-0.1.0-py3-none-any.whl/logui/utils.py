from __future__ import annotations

import logging
import os


def check_loggers(LOGGING: dict) -> None:
    if os.environ.get('RUN_MAIN') != 'true':
        for logger_name in LOGGING['loggers']:
            log = logging.getLogger(logger_name)
            log.warning(f'Logger found: {logger_name}')
