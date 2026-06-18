from testcontainers.postgres import PostgresContainer


class Container(PostgresContainer):
    def __init__(self, **kwargs):
        if not hasattr(kwargs, 'healthcheck'):
            kwargs['healthcheck'] = {
                "test": ["CMD", "pg_isready", "-U", "postgres"]
            }
        super().__init__(**kwargs)
        self.waiting_for(HealthcheckWaitStrategy())

    @property
    def exposed_port(self):
        return self.get_exposed_port(self.port)
