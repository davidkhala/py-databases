from pymongo import MongoClient
from pymongo.errors import OperationFailure

from davidkhala.data.base.__init__ import Connectable

class Client(Connectable):

    def __init__(self, connection_string):
        super().__init__()
        self.client = MongoClient(connection_string)


    def connect(self):
        try:
            r = self.client.admin.command('ping')
            assert r == {'ok': 1}
            return True
        except OperationFailure as e:
            if e.code == 8000 and e.details.get('errmsg')=='bad auth : authentication failed':
                return False
            raise e