# FIXME: to be modulized
from pprint import pprint
import requests
from requests import Response

restHostname = "rest_hostname"
dbHostname = "db_hostname"
username = "username"
password = "password"
token = ""

def authenticate():
    global token
    url = "https://%s:50050/v1/auth"% (restHostname)
    json = {
        "dbParms": {
            "dbHost": dbHostname,
            "dbName": "BLUDB",
            "dbPort": 50001,
            "isSSLConnection": True,
            "username": username,
            "password": password,
        },
        "expiryTime": "24h"
    }
    response = requests.post(url, verify = False, json = json, proxies = None)
    if response.status_code == 200:
        token = response.json()["token"]
        print("Authenticated user with token:", token)