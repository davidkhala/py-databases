from testcontainers.mysql import MySqlContainer


class Container(MySqlContainer):
    def __init__(self, **kwargs):
        if hasattr(kwargs, 'healthcheck'):
            kwargs['healthcheck'] = {
                "test": ["CMD", "mysqladmin", "ping","-uroot","-p$MYSQL_ROOT_PASSWORD",  "-h", "localhost"]
            }
        super().__init__(**kwargs)