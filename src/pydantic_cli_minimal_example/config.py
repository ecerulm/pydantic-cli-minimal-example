import os
from enum import Enum
from pathlib import Path
from typing import Annotated, override

import jwt
from pydantic import AfterValidator, model_validator
from pydantic.types import Secret
from pydantic_settings import BaseSettings, CliSubCommand, SettingsConfigDict
from typing_extensions import Self


class JsonWebTokenBase(
    Secret[str]
):  # This is not a Model so you can't use model_validator

    @override
    def _display(self) -> str:
        # return "".join(["*" for x in self.get_secret_value()])

        sub = jwt.decode(
            self.get_secret_value(),
            options={
                "verify_signature": False,
            },
        ).get("sub")
        return f"JWT sub: {sub}"


def validate_jwt(v: str) -> str:
    try:
        jwt.decode(
            v.get_secret_value(),
            options={
                "verify_signature": False,
                "verify_iat": True,
                # "verify_exp": True,
                "verify_nbf": True,
            },
        )

        return v
    except jwt.exceptions.InvalidTokenError as e:
        raise ValueError(e)


JsonWebToken = Annotated[JsonWebTokenBase, AfterValidator(validate_jwt)]


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
    jwt: JsonWebToken

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
