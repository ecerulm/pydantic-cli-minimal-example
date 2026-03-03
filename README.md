# run 

```
uv run myapp --help
Usage: myapp [-h] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--requests-log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--log-dir Path]
             [--log-file str]

options:
  -h, --help            show this help message and exit
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        (default: INFO)
  --requests-log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        (default: WARNING)
  --log-dir Path        (default: ./logs)
  --log-file str        (default: log)
```

```
uv run myapp --requests-log-level DEBUG
2026-03-03T18:12:07.318627+01:00 - myapp - INFO - settings: {"log_level":"INFO","requests_log_level":"DEBUG","log_dir":"logs","log_file":"log"}
2026-03-03T18:12:07.322143+01:00 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): google.com:443
2026-03-03T18:12:07.396552+01:00 - urllib3.connectionpool - DEBUG - https://google.com:443 "GET / HTTP/1.1" 301 220
2026-03-03T18:12:07.397286+01:00 - urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): www.google.com:443
2026-03-03T18:12:07.484733+01:00 - urllib3.connectionpool - DEBUG - https://www.google.com:443 "GET / HTTP/1.1" 200 None
```

# Setup

```
uv init --package --python ">=3.13,<3.14"
uv add pydantic pydantic-settings
uv add --dev pytest mypy
```


