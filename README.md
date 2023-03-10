# Filmscape

Filmscape is proof-of-concept for video library application backend written in Django.

## Environment variables for docker-compose
- `API_URL`: Address of external API **(required)**.
- `LOGGING_LEVEL`: Severity of logged information (possible values: debug, info, warning, danger, critical; default: info).
- `SYNC_TIMEOUT`: Number of minutes between repeated fetching of data from the external API (default: 60).
- `DEBUG`: Use value "True" to run the app in the debug mode.