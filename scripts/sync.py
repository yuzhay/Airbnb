import json
import time
import pprint
from datetime import date, datetime, timedelta
import phonenumbers
from phonenumbers.phonenumberutil import (
    region_code_for_country_code,
    region_code_for_number,
)
import pycountry
from models import *
from airbnb import add_months


class Sync:
  """Full synchronizer
  """

  DATE_FORMAT = '%Y-%m-%d'
  DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
  STEPS = [
    'users',
    'listings',
    'threads',
    'reservations',
    'hosting_activities',
    'host_earnings',
  ]

  _db = None
  _user = None
  _listings = None
  _timer = None


  def __init__(self, db, airbnb, sync_listings = {}):
    """Constructor
    """

    self._db = db
    self._airbnb = airbnb
    self._timer = time.time()
    self._sync_listings = sync_listings
    self._start_sync_date = None
    self._force = False


  def console(self, msg):
    """Print console
    """

    print("[{0:0.2f}]\t{1}".format(time.time() - self._timer, msg))


  def json_print(self, param):
    print(json.dumps(param, indent=2, sort_keys=True))


  def run(self, force = False):
    """Run synchronization
    """

    self._force = force

    if not force:
      self._start_sync_date = date.today() - timedelta(3)

    SyncLog.start(self._db)
    self.console("Syncing started")

    for step in self.STEPS:
      getattr(self, step)()
      self.console(step + " syncronized")

    self.console("Syncing finished")
    SyncLog.finish(self._db)


  def users(self):
    """Sync users
    """

    self._user = self._airbnb.get_profile()['login']['account']['user']
    params = {key: self._user[key] for key in ['id', 'first_name', 'last_name', 'created_at']}
    params['registered_at'] = params.pop('created_at')
    User.update_or_create(self._db, params)


  def listings(self):
    """Sync listings
    """

    listings = self._airbnb.listings()['listings']
    self._listings = list(filter(lambda listing : listing['id'] in self._sync_listings, listings))

    for listing in self._listings:
      params = {
        'id': listing['id'],
        'name': listing['name'],
        'user_id': self._user['id']
      }
      Listing.update_or_create(self._db, params)

      start_date = self.__max_date(self._sync_listings[listing['id']]['start_date'], self._start_sync_date)

      now = datetime.now().date()
      date_index = start_date

      while (date_index < now):
        demands_json = self._airbnb.listing_trip_demands(listing['id'], date_index)
        demands = demands_json['listing_trip_demand']['monthly_trip_demand_counts'][0]['daily_trip_demand_counts']

        for demand in demands:
          params = {
            'listing_id': listing['id'],
            'booked': demand['booked'],
            'bookings': demand['bookings'],
            'date': demand['date'],
            'inquiries': demand['inquiries'],
            'page_views': demand['page_views'],
            'unavailable': demand['unavailable']
          }
          Demand.update_or_create(self._db, params)

        date_index = add_months(date_index)


  def threads(self):
    """Sync Threads
    """

    total_pages = 0
    offset = 0
    page = 0
    while True:
      response = self._airbnb.threads(offset)
      total_pages = int(response['metadata']['num_pages'])
      threads = response['threads']

      for t in threads:
        other_user = t['other_user']
        guest = {
          'id': other_user['id'],
          'first_name': other_user['first_name']
        }

        Guest.update_or_create(self._db, guest)

        params = {
          'id': t['id'],
          'user_id': self._user['id'],
          'status': t['status'],
          'unread': t['unread'],
          'other_user_id': t['other_user']['id'],
        }
        Thread.update_or_create(self._db, params)

      offset += len(threads)
      page += 1
      if page >= total_pages or not self._force:
        break

  def reservations(self):
    """Sync Reservations
    """

    offset = 0
    if self._start_sync_date != None:
      date_min = self._start_sync_date.strftime(self.DATE_FORMAT)
    else:
      date_min = None

    while True:
      response = self._airbnb.reservations(offset, 40, date_min)
      total_count = response['metadata']['total_count']
      reservations = response['reservations']

      for reserve in reservations:
        guest = reserve['guest_user']
        country = self.__get_country_by_phone(guest.get('phone'))
        guest = { **guest, **country }

        Guest.update_or_create(self._db, guest)

        earnings = reserve['earnings'].replace('€','')

        self.__create_default_listing(reserve['listing_id'])
        self.__create_default_thread(reserve['thread_id'])
        params = {
          'confirmation_code':        reserve['confirmation_code'],
          'thread_id':                reserve['thread_id'],
          'start_date':               reserve['start_date'],
          'end_date':                 reserve['end_date'],
          'listing_id':               reserve['listing_id'],
          'earnings':                 earnings,
          'nights':                   reserve['nights'],
          'booked_date':              reserve['booked_date'],
          'host_vat_invoices':        json.dumps(reserve['host_vat_invoices']),
          'guest_id':                 reserve['guest_user']['id'],
          'user_facing_status_key':   reserve['user_facing_status_key']
        }
        Reservation.update_or_create(self._db, params)
      offset += len(reservations)
      if offset >= total_count:
        break


  def hosting_activities(self):
    """Sync HostingActivities
    """

    date_index = datetime.strptime(self._user['created_at'], self.DATETIME_FORMAT).date()
    date_index = self.__max_date(date_index, self._start_sync_date)

    while date_index < add_months(datetime.now(), 3):
      params = {
        'year': date_index.year,
        'month': date_index.month
      }
      ha = self._airbnb.hosting_activities(**params)['hosting_activities'][0]

      activity = {
        'year': ha['year'],
        'month': ha['month'],
        'nights_booked': ha['nights_booked'],
        'nights_unbooked': ha['nights_unbooked'],
        'occupancy_rate': ha['occupancy_rate'],
        'cleaning_fees': ha['cleaning_fees']['amount']
      }
      if ha['nights_price_range'] != None:
        activity['nights_price_min'] = ha['nights_price_range'][0]['amount'],
        activity['nights_price_max'] = ha['nights_price_range'][1]['amount']
      else:
        activity['nights_price_min'] = None
        activity['nights_price_max'] = None

      HostingActivity.update_or_create(self._db, activity)
      date_index = add_months(date_index)


  def host_earnings(self):
    """Sync HostEarnings
    """

    date_index = datetime.strptime(self._user['created_at'], self.DATETIME_FORMAT).date()
    date_index = self.__max_date(date_index, self._start_sync_date)

    while date_index < add_months(datetime.now(), 3):
      params = {
        'year': date_index.year,
        'month': date_index.month
      }
      he = self._airbnb.host_earnings(**params)['host_earnings'][0]

      earning = {
        'year': he['year'],
        'month': he['month'],
        'cancellation_fees': he['cancellation_fees']['amount'],
        'cohosting_earnings': he['cohosting_earnings']['amount'],
        'paid_out': he['paid_out'][0]['amount'],
        'pending': he['pending'][0]['amount'],
        'total': he['total'][0]['amount']
      }

      HostEarning.update_or_create(self._db, earning)
      date_index = add_months(date_index)


  def __create_default_thread(self, id):
    if not Thread.exists(self._db, {'id': id }):
      Thread.create(self._db, {
        'id': id,
        'user_id': self._user['id'],
        'status': 'removed',
        'other_user_id': 0,
        'unread': False
      })

  def __create_default_listing(self, id):
    if not Listing.exists(self._db, {'id': id}):
      Listing.create(self._db, {
          'id': id,
          'user_id': self._user['id'],
          'name': 'Removed'
        }
      )

  def __get_country_by_phone(self, phone):
    if phone == None:
      return {}

    pn = phonenumbers.parse(phone)
    country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
    return {
      'region_code': region_code_for_country_code(pn.country_code),
      'country': country.name
    }

  def __max_date(self, date1, date2):
    if date1 == None and date2 == None:
      return None

    if date1 == None:
      return date2

    if date2 == None:
      return date1

    return max(date1, date2)
