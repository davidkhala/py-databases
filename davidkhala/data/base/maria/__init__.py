from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

def rewrite_connection_string(connection_string: str) -> str:
    parsed = urlparse(connection_string)
    new_url = parsed._replace(
        scheme='mariadb+mariadbconnector',
    )

    return urlunparse(new_url)
