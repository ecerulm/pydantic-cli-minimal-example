import logging

from .config import get_settings

logger = logging.getLogger("myapp")


def main() -> None:
    settings = get_settings()
    logger.info("settings: %s", settings)
