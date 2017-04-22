#!/usr/bin/env python3

from common import *

#print(json.dumps(p, indent=2, sort_keys=True))

class Sync:
    _db = None
    _user = None
    _listings = None

    def __init__(self, db):
        self._db = db

    def run(self):
        SyncLog.start(self._db)
        self.users()
        self.listings(date(2016,8,1))
        self.threads()
        self.reservation_requests()
        SyncLog.finish(self._db)

    def users(self):
        self._user = airbnb.get_profile()['user']
        User.update_or_create(self._db, self._user['id'], self._user['first_name'], self._user['last_name'])

    def listings(self, date_index):
        self._listings = airbnb.listings()['listings']

        for listing in self._listings:
            Listing.update_or_create(self._db, listing['id'], listing['name'], self._user['id'])

            start_date = datetime.strptime(self._user['created_at'], DATETIME_FORMAT).date()
            now = datetime.now().date()

            while (date_index < now):
                demands_json = airbnb.listing_trip_demands(listing['id'], date_index)
                demands = demands_json['listing_trip_demand']['monthly_trip_demand_counts'][0]['daily_trip_demand_counts']

                for demand in demands:
                    Demand.update_or_create(self._db, listing['id'], demand['booked'], demand['bookings'], demand['date'], demand['inquiries'], demand['page_views'], demand['unavailable'])

                date_index = add_months(date_index)

    def threads(self):
        thread_index = 0
        while True:
            response = airbnb.threads(thread_index)
            total_threads = int(response['thread_count'])
            threads = response['threads']
            for t in threads:
                t = t['thread']
                if not Thread.exists(self._db, t['id']):
                    Thread.create(self._db, t['id'], user['id'], t['status'], t['unread'],
                       t['responded'], t['other_user']['user']['id'],
                       t['other_user']['user']['first_name'], t['preview'], t['updated_at'])

            thread_index += len(threads)
            if thread_index >= total_threads:
                break

    def reservation_requests(self):
        self._threads = Thread.get_all(self._db)
        for thread in self._threads:
             response = airbnb.reservation_requests(thread[0])
             if response['reservation'] is None:
                 continue

             reservation = response['reservation']['reservation']
             thread = response['thread']['thread']
             guest = reservation['guest']['user']
             host_user = reservation['host']['user']
             listing = reservation['listing']['listing']

             if ReservationRequest.exists(self._db, reservation['id']):
                 continue

             ReservationRequest.create(self._db,
                reservation['id'],
                reservation['thread_id'],
                thread['inquiry_checkin_date'],
                thread['inquiry_checkout_date'],
                thread['inquiry_number_of_guests'],
                thread['inquiry_price_native'],
                listing['id'],
                listing['price'],
                guest['id'],
                reservation['native_currency'],
                reservation['instant_bookable'],
                host_user['is_superhost'],
                guest['identity_verified'],
                guest['created_at'],
                reservation['status'])

# def f(**params):
#     print(params)
#
# def d(a):
#     print(a['a'])
#
# f(a=1,b=2)
#
# a = {'a': 1}
# f(**a)
