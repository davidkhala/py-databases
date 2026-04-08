from astrapy import DataAPIClient, AstraDBAdmin
from astrapy.exceptions import DevOpsAPIHttpException


class Client:
    def __init__(self, token: str):
        super().__init__()
        self.client = DataAPIClient(token)
        self.token: str = token

    def connect(self, api_endpoint) -> bool:
        db = self.client.get_database(
            api_endpoint,
            token=self.token
        )

        try:
            db.info()
            self.db = db
            return True
        except DevOpsAPIHttpException as e:
            assert e.text.startswith('Resource, token, was malformed.')
            return False
