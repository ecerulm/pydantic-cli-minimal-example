import os
from enum import Enum
from pathlib import Path

from pydantic_settings import BaseSettings, CliSubCommand, SettingsConfigDict


# This enum provides validation
class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class CanoodleSettings(BaseSettings):
    pass


class DrizzleSettings(BaseSettings):
    pass


class AppSettings(BaseSettings):
    canoodle: CliSubCommand[CanoodleSettings]
    drizzle: CliSubCommand[DrizzleSettings]

    # configurable log levels for different loggers
    log_level: LogLevel = LogLevel.INFO
    requests_log_level: LogLevel = LogLevel.WARNING
    log_dir: Path = Path("./logs")
    log_file: str = "log"

    model_config = SettingsConfigDict(
        env_file=".env",  # load settings / configuration parameters if it exists
        cli_parse_args=True,
        cli_exit_on_error=True,
        cli_prog_name="myapp",
        # cli_implicit_flags -> --flag / --no-flag
        cli_implicit_flags=True,  # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#cli-boolean-flags
        cli_kebab_case=True,  # https://docs.pydantic.dev/latest/concepts/pydantic_settings/#cli-kebab-case-for-arguments
    )


if os.environ.get("PYTEST_VERSION") is not None:
    settings = AppSettings(
        canoodle=CanoodleSettings(),
        drizzle=DrizzleSettings(),
        _env_file=None,
        _cli_parse_args=False,
        _cli_exit_on_error=False,
    )
else:
    settings = AppSettings()
