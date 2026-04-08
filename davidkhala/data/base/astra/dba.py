from astrapy import AstraDBAdmin

from davidkhala.data.base.astra import Client


class DBA:

    def __init__(self, client: Client):
        self._: AstraDBAdmin = client.client.get_admin()
