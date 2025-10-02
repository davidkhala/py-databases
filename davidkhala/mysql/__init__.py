from davidkhala.sql import SQL
import importlib.util
from urllib.parse import urlparse, urlunparse

# dependency: (driver, module)
MYSQL_DRIVERS = {
    "mysqlclient": ("mysqldb", "MySQLdb"),
    "pymysql": ("pymysql", "pymysql"),
    "mysql-connector-python": ("mysqlconnector", "mysql.connector"),
    "asyncmy": ("asyncmy", "asyncmy"),
    "aiomysql": ("aiomysql", "aiomysql")
}

PREFERRED_ORDER = ["mysqlclient", "pymysql", "mysql-connector-python"]  # "mysqlclient" is sqlalchemy default


def detect_installed_driver():
    for key in PREFERRED_ORDER:
        _, module_name = MYSQL_DRIVERS[key]
        if importlib.util.find_spec(module_name):
            return MYSQL_DRIVERS[key][0]
    raise RuntimeError("No supported MySQL driver found in current venv.")


def rewrite_connection_string(connection_string: str):
    parsed = urlparse(connection_string)
    dialect_driver = parsed.scheme

    if '+' in dialect_driver:
        dialect, _ = dialect_driver.split('+', 1)
    else:
        dialect = dialect_driver

    new_driver = detect_installed_driver()
    new_scheme = f"{dialect}+{new_driver}"

    new_url = parsed._replace(scheme=new_scheme)
    return urlunparse(new_url)


class Mysql(SQL):
    def __init__(self, connection_string: str):
        super().__init__(rewrite_connection_string(connection_string))
