from davidkhala.data.base.sql import SQL


class DBA:

    def __init__(self, instance: SQL):
        self._ = instance

    @property
    def version(self) -> str:
        r = self._.query("select service_level from sysibmadm.env_inst_info")
        return r.scalars().one()
