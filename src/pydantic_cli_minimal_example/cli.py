import logging

import requests
from pydantic_settings import get_subcommand

from .config import CanoodleSettings, DrizzleSettings, get_settings
from .logconfig import setup_handlers

logger = logging.getLogger("myapp")


def canoodle(settings: CanoodleSettings) -> None:
    logger.info("canoodle")


def drizzle(settings: DrizzleSettings) -> None:
    logger.info("drizzle")


def main() -> None:
    settings = get_settings()

    subcommand = get_subcommand(settings)
    if isinstance(subcommand, CanoodleSettings):
        canoodle(subcommand)
    elif isinstance(subcommand, DrizzleSettings):
        drizzle(subcommand)

    setup_handlers()

    requests_log_level = settings.requests_log_level
    requests_numeric_level = getattr(logging, requests_log_level.upper(), logging.INFO)
    logging.getLogger("urllib3").setLevel(requests_numeric_level)
    logger.info("settings: %s", settings.model_dump_json())
    r = requests.get("https://google.com")
