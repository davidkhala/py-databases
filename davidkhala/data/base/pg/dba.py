from davidkhala.data.base.pg import Postgres


class DBA:

    def __init__(self, pg: Postgres):
        self._ = pg

    @property
    def databases(self):
        r = self._.query("SELECT datname FROM pg_database where datistemplate = FALSE")
        return r.scalars().all()

