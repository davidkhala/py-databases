from abc import abstractmethod, ABC
from typing import Union, Optional, Any


class Connectable(ABC):
    def __init__(self, *args, **kwargs):
        self.connect_string: str
        self.client: Any
        self.connection: Any

    @abstractmethod
    def connect(self, *args, **kwargs):
        ...

    @abstractmethod
    def disconnect(self):
        ...

    @staticmethod
    def connect_string(
            dialect: str, domain: str,
            *,
            driver: Optional[str]=None,
            port: Optional[Union[str, int]]=3306,
            username: Optional[str],
            password: Optional[str],
            name: Optional[str]=None,
            queries: Optional[dict]= None
    ):

        auth = ''
        if username:
            auth += username
            if password:
                auth += f':{password}'
            auth += '@'

        base = f"{dialect}{'+' + driver if driver else ''}://{auth}{domain}{':' + str(port) if port else ''}{'/' + name if name else ''}"

        if queries:
            query_string = '&'.join(f"{key}={value}" for key, value in queries.items())
            return f"{base}?{query_string}"
        else:
            return base
