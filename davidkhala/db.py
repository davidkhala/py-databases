from abc import abstractmethod
from typing import Union, Optional


class Connectable:
    def __init__(self, password: str, username: str, domain: str = 'localhost', tls: bool = True):
        ...

    @staticmethod
    def connectString(
            dialect:str, domain:str,
            *,
            driver:Optional[str],port:Optional[Union[str, int]], username:Optional[str], password:Optional[str], name:Optional[str]
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
