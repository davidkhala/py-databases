from davidkhala.data.base.sql import SQL
import importlib.util
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# dependency: (driver, module)
PG_DRIVERS = {
    "psycopg2": ("psycopg2", "psycopg2"),
    "psycopg": ("psycopg", "psycopg"),  # psycopg3
    "pg8000": ("pg8000", "pg8000"),
    "asyncpg": ("asyncpg", "asyncpg")
}

# psycopg2 is default driver of SQLAlchemy
PREFERRED_ORDER = ["psycopg2", "psycopg", "pg8000"]


def detect_installed_driver():
    for key in PREFERRED_ORDER:
        _, module_name = PG_DRIVERS[key]
        if importlib.util.find_spec(module_name):
            return PG_DRIVERS[key][0]
    raise RuntimeError("No supported PostgreSQL driver found in current venv.")


def rewrite_connection_string(connection_string: str) -> str:
    parsed = urlparse(connection_string)
    dialect_driver = parsed.scheme

    if '+' in dialect_driver:
        dialect, _ = dialect_driver.split('+', 1)
    else:
        dialect = dialect_driver

    new_driver = detect_installed_driver()

    query = dict(parse_qsl(parsed.query))

    new_url = parsed._replace(
        scheme=f"{dialect}+{new_driver}",
        query=urlencode(query)
    )
    return str(urlunparse(new_url))


class Postgres(SQL):
    def __init__(self, connection_string: str):
        super().__init__(rewrite_connection_string(connection_string))
