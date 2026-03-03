import logging

import requests

from .config import get_settings
from .logconfig import setup_handlers

logger = logging.getLogger("myapp")


def main() -> None:
    settings = get_settings()
    setup_handlers()
    logger.info("settings: %s", settings.model_dump_json())

    requests_log_level = settings.requests_log_level
    requests_numeric_level = getattr(logging, requests_log_level.upper(), logging.INFO)
    logging.getLogger("urllib3").setLevel(requests_numeric_level)

    r = requests.get("https://google.com")
