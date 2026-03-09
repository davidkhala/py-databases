from testcontainers.core.wait_strategies import HealthcheckWaitStrategy
from testcontainers.mysql import MySqlContainer


class Container(MySqlContainer):
    def __init__(self, **kwargs):
        if not hasattr(kwargs, 'healthcheck'):
            kwargs['healthcheck'] = {
                "test": ["CMD", "mysqladmin", "ping","-uroot","-p$MYSQL_ROOT_PASSWORD",  "-h", "localhost"]
            }
        super().__init__(**kwargs)
    def start(self):
        self.waiting_for(HealthcheckWaitStrategy())
        super().start()