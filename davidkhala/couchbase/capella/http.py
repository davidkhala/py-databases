from davidkhala.http_request import Request

BaseURL = 'https://cloudapi.cloud.couchbase.com/v4/organizations'


class API(Request):
    def __init__(self, route, api_secret):
        super().__init__(BaseURL + route, {
            'bearer': api_secret
        })

        self.secret = api_secret

    def set_route(self, route):
        self.url = BaseURL + route

