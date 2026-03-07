# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run myapp --help          # run the CLI
uv run myapp canoodle        # run the canoodle subcommand
uv run myapp drizzle         # run the drizzle subcommand
uv run pytest                # run tests
uv run mypy .                # type-check (uses venv mypy to resolve types-requests)
```

## Architecture

The entry point is `pydantic_cli_minimal_example:main` (defined in `__init__.py` → `cli.py`).

**Configuration & CLI parsing** (`config.py`): All CLI arguments and env/dotfile settings are declared as a single `AppSettings(BaseSettings)` model using `pydantic-settings`. `cli_parse_args=True` makes pydantic-settings own `sys.argv` parsing — no argparse or click involved. Subcommands are declared as `CliSubCommand[XSettings]` fields on `AppSettings`. Add new subcommands here by creating a `BaseSettings` subclass and adding a `CliSubCommand` field.

**Dispatch** (`cli.py`): After parsing, `get_subcommand(settings)` returns the active subcommand instance. Use `isinstance` checks to dispatch to the appropriate handler function.

**Logging** (`logconfig.py`): `setup_handlers()` replaces all root logger handlers. Outputs to console (colorized text if TTY, JSONL otherwise), a daily-rotating `.txt` file, and a size-rotating `.jsonl` file. Call `setup_handlers()` after `get_settings()` so settings are available.

**Settings singleton**: `get_settings()` caches the `AppSettings` instance. Since `AppSettings` parses `sys.argv` on construction, it must only be instantiated once.
