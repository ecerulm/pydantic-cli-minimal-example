from collections.abc import Iterator

import pytest
from pydantic_core import PydanticUndefined
from pytest import FixtureRequest

import pydantic_cli_minimal_example.config as config_module
from pydantic_cli_minimal_example.cli import main
from pydantic_cli_minimal_example.config import AppSettings, LogLevel, settings


@pytest.fixture
def patch_settings(request: FixtureRequest) -> Iterator[AppSettings]:
    # This fixture will overwrite update settings object temporarily

    # Make a copy of the original settings
    original_settings = settings.model_copy()

    # The fixture can introspect the requesting test context
    # https://docs.pytest.org/en/stable/how-to/fixtures.html#fixtures-can-introspect-the-requesting-test-context

    # Overwrite the settings to use the default values
    for k, v in AppSettings.model_fields.items():
        setattr(settings, k, v.default)

    yield settings  # https://docs.pytest.org/en/stable/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization

    # Restore the original settings
    settings.__dict__.update(original_settings.__dict__)


def test_canoodle_is_called_for_canoodle_subcommand(patch_settings):
    # With the patch_settings fixture the settings object is cleared it won't read from .env or environment variables
    assert settings.canoodle is PydanticUndefined
    assert settings.drizzle is PydanticUndefined
    assert settings.log_level == LogLevel.INFO
