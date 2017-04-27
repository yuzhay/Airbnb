import requests
import json
from datetime import datetime, date, time

API_URL = "https://api.airbnb.com"
MAIN_URL = "https://airbnb.com"
CLIENT_ID = "3092nxybyb0otqw18e8nh5nty"
KEY = "d306zoyjsyarp7ifhu67rjxn52tv0t20"

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

    def listings(self, limit=10, offset=0, has_availability=False):
        r = self._session.get(API_URL + "/v2/listings",
            params = {
                '_limit': limit,
                '_offset': offset,
                'currency': str(self._currency),
                'user_id': str(self.uid),
                'has_availability': str(has_availability)
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
                'key': KEY,
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

    # /v2/hosting_activities
    #       ?year=2017
    #       &period=yearly
    #       &key=d306zoyjsyarp7ifhu67rjxn52tv0t20
    #       &currency=EUR
    #       &locale=en
    # https://www.airbnb.com/api/v2/hosting_activities?year=2016&period=monthly&month=9&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=EUR&locale=en

    def hosting_activities(self, year, period = "yearly"):
        r = self._session.get(API_URL + "/v2/hosting_activities",
            params = {
                'key': KEY,
                'currency': str(self._currency),
                'period': period,
                'year': year
            })
        r.raise_for_status()
        return r.json()

    # /v2/host_earnings
    #       ?_format=for_web_host_stats
    #       &year=2017
    #       &period=yearly
    #       &key=d306zoyjsyarp7ifhu67rjxn52tv0t20
    #       &currency=EUR
    #       &locale=en

    # /v2/host_earnings
    #       ?_format=for_web_host_stats
    #       &left_offset=0
    #       &right_offset=11
    #       &month=1
    #       &year=2017
    #       &key=d306zoyjsyarp7ifhu67rjxn52tv0t20
    #       &currency=EUR
    #       &locale=en

    def host_earnings(self, year, period = "yearly"):
        r = self._session.get(API_URL + "/v2/host_earnings",
            params = {
                '_format': 'for_web_host_stats',
                'key': KEY,
                'currency': str(self._currency),
                'period': period,
                'year': year
            })
        r.raise_for_status()
        return r.json()

    # https://www.airbnb.com/transaction_history/45501729
    #   ?year=2017
    #   &start_month=1&
    #   end_month=12
    #   &for_payout_tracker=true
    #   &page=1

    # def transaction_history(self):
    #     r = self._session.get(MAIN_URL + "/transaction_history",
    #         params = {
    #             '_format': 'for_web_host_stats',
    #             'key': KEY,
    #             'currency': str(self._currency),
    #             'period': period,
    #             'year': year
    #         })
    #     r.raise_for_status()
    #     return r.json()
