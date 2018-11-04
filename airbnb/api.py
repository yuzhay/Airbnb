import requests
import json
import pprint
from datetime import datetime, date, time
from . import exceptions

API_URL = "https://api.airbnb.com/v2"
API_KEY = "915pw2pnf4h1aiguhph5gc5b2"
KEY = "d306zoyjsyarp7ifhu67rjxn52tv0t20"

class Api(object):
  def __init__(self, username=None, password=None, uid=None, access_token=None, api_key=API_KEY, session_cookie=None, currency='EUR'):
    self._session = requests.Session()
    self._currency = currency
    self._session.headers = self.__headers(api_key, currency)

    if access_token:
      self._access_token = access_token
      if session_cookie and "_airbed_session_id=" in session_cookie:
        self._session.headers.update({ "Cookie": session_cookie })
      self._session.headers.update({"x-airbnb-oauth-token": self._access_token })
    else:
      assert(username and password)
      login_payload = {
        "email": username,
        "password": password,
        "type": "email"
      }

      r = self._session.post(API_URL + "/logins", data=json.dumps(login_payload))

      if r.status_code == 420:
        raise exceptions.VerificationException
      elif r.status_code == 403:
        raise exceptions.AuthenticationException

      self._access_token = r.json()["login"]["id"]
      self.uid = r.json()["login"]["account"]["id"]

      self._session.headers.update({"x-airbnb-oauth-token": self._access_token})

  def __headers(self, api_key, currency = "EUR", country = "us"):
    return {
      "accept": "application/json",
      "accept-encoding": "gzip, deflate",
      "content-type": "application/json",
      "user-agent": "Airbnb/18.38 AppVersion/18.38 iPhone/12.0 Type/Phone",
      "x-airbnb-api-key": api_key,
      "x-airbnb-screensize": "w=375.00;h=812.00",
      "x-airbnb-carrier-name": "T-Mobile",
      "x-airbnb-network-type": "wifi",
      "x-airbnb-currency": currency,
      "x-airbnb-locale": "en",
      "x-airbnb-carrier-country": country,
      "accept-language": "en-us"
    }

  def get_profile(self):
    assert(self._access_token)
    r = self._session.get(API_URL + "/logins/me")
    r.raise_for_status()
    return r.json()

  def listings(self, limit=10, offset=0, has_availability=False):
    assert(self._access_token)
    r = self._session.get(API_URL + "/listings",
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
    assert(self._access_token)
    r = self._session.get(API_URL + "/listings",
      params = {
        'currency': str(self._currency),
        'has_availability': str(False),
        'user_id': str(self.uid),
        '_offset': 0,
        '_limit': 1,
        'listing_ids[]': listing_id
      })
    r.raise_for_status()
    return r.json()

  def listing_trip_demands(self, listing_id, date ):
    assert(self._access_token)
    year = date.year
    month = date.month
    day = date.day
    r = self._session.get(
      API_URL + "/listing_trip_demands/{0}/{1}/{2}/{3}/bysearchdate".format(listing_id, year, month, day),
      params = {
        'key': KEY,
        'currency': str(self._currency)
      })
    r.raise_for_status()

    if r.status_code != 200:
      return None

    return r.json()

  def threads(self, offset = 0, items_per_page = 10):
    assert(self._access_token)
    r = self._session.get(API_URL + "/threads",
      params = {
        '_offset': offset,
        'items_per_page': items_per_page,
        'currency': str(self._currency),
        '_format': 'for_web_inbox'
      })
    r.raise_for_status()
    return r.json()

  def reservations(self, offset = 0, limit = 40, date_min = None):
    assert(self._access_token)

    params = {
      '_offset': offset,
      '_limit': limit,
      'currency': str(self._currency),
      '_format': 'for_reservations_list',
      'collection_strategy': 'for_reservations_list',
      'key': KEY
    }

    if date_min != None:
      params['date_min'] = date_min

    r = self._session.get(API_URL + "/reservations", params = params)
    r.raise_for_status()
    return r.json()

  def hosting_activities(self, **args):
    assert(self._access_token)
    params = {
      'key': KEY,
      'currency': str(self._currency),
      'period': 'monthly'
    }
    params.update(args)

    r = self._session.get(API_URL + "/hosting_activities", params = params)
    r.raise_for_status()
    return r.json()


  def host_earnings(self, **args):
    assert(self._access_token)
    params = {
      '_format': 'for_web_host_stats',
      'key': KEY,
      'currency': str(self._currency),
      'period': 'monthly',
      'year': datetime.now().year
    }
    params.update(args)
    r = self._session.get(API_URL + "/host_earnings", params = params)
    r.raise_for_status()
    return r.json()
