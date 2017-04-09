import requests
import json
from datetime import datetime, date, time

API_URL = "https://api.airbnb.com"
CLIENT_ID = "3092nxybyb0otqw18e8nh5nty"

class AuthError(Exception):
    """
    Authentication error
    """
    pass

class Api(object):
    def __init__(self, username=None, password=None, uid=None, access_token=None, currency='EUR'):
        self._session = requests.Session()
        self._session.headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json"
        }
        self._currency = currency
        if uid and access_token:
            self.uid = uid
            self._access_token = access_token
            self._session.headers.update({
                "X-Airbnb-OAuth-Token": self._access_token
            })
        else:
            login_payload = {
                "username": username,
                "password": password,
                "prevent_account_creation": "true"
            }
            r = self._session.post(
                API_URL + "/v1/authorize",
                params = {
                    'client_id': CLIENT_ID,
                    'currency': currency
                },
                data=json.dumps(login_payload)
            )
            if "access_token" not in r.json():
                raise AuthError
            r.raise_for_status()
            self._access_token = r.json()["access_token"]
            self._session.headers.update({
                "X-Airbnb-OAuth-Token": self._access_token
            })
            r = self._session.get(API_URL + "/v1/account/active")
            r.raise_for_status()
            self.uid = r.json()["user"]["user"]["id"]

    def get_profile(self):
        r = self._session.get(API_URL + "/v1/users/" + str(self.uid))
        r.raise_for_status()
        return r.json()

    def listings(self, limit=10, offset=0):
        r = self._session.get(API_URL + "/v2/listings",
            params = {
                '_limit': limit,
                '_offset': offset,
                'currency': str(self._currency),
                'user_id': str(self.uid)
            })
        r.raise_for_status()
        return r.json()

    def listing(self, listing_id):
        r = self._session.get(API_URL + "/v2/listings/" + str(listing_id),
            params = {
                'currency': str(self._currency),
                'user_id': str(self.uid),
                '_format': 'v1_legacy_for_p3'
            })
        r.raise_for_status()
        return r.json()

    def listing_trip_demands(self, listing_id, date ):
        year = date.year
        month = date.month
        day = date.day
        r = self._session.get(
            API_URL + "/v2/listing_trip_demands/{0}/{1}/{2}/{3}/bysearchdate".format(listing_id, year, month, day),
            params = {
                'key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
                'currency': str(self._currency)
            })
        r.raise_for_status()
        return r.json()

    def threads(self, offset = 0, items_per_page = 100):
        r = self._session.get(API_URL + "/v1/threads",
            params = {
                'offset': offset,
                'items_per_page': items_per_page,
                'currency': str(self._currency)
            })
        r.raise_for_status()
        return r.json()

    def reservation_requests(self, thread_id):
        r = self._session.get(API_URL + "/v1/reservations/relationship",
            params = {
                'thread_id': thread_id,
                'currency': str(self._currency)
            })
        r.raise_for_status()
        return r.json()
