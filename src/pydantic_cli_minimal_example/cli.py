import logging

import requests
from pydantic_settings import get_subcommand

from .config import CanoodleSettings, DrizzleSettings, settings
from .logconfig import setup_handlers

logger = logging.getLogger("myapp")


def canoodle(settings: CanoodleSettings) -> None:
    logger.info("canoodle")
    r = requests.get("https://google.com")


def drizzle(settings: DrizzleSettings) -> None:
    logger.info("drizzle")
    r = requests.get("https://google.com")


def main() -> None:
    requests_log_level = settings.requests_log_level
    requests_numeric_level = getattr(logging, requests_log_level.upper(), logging.INFO)
    logging.getLogger("urllib3").setLevel(requests_numeric_level)
    setup_handlers()
    logger.info("settings: %s", settings.model_dump_json())

    subcommand = get_subcommand(settings)

    if isinstance(subcommand, CanoodleSettings):
        canoodle(subcommand)
    elif isinstance(subcommand, DrizzleSettings):
        drizzle(subcommand)
