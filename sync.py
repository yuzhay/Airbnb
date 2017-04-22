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
        User.update_or_create(self._db, **self._user)

    def listings(self, date_index):
        self._listings = airbnb.listings()['listings']

        for listing in self._listings:
            params = {
                'id': listing['id'],
                'name': listing['name'],
                'user_id': self._user['id']
            }
            Listing.update_or_create(self._db, **params)

            start_date = datetime.strptime(self._user['created_at'], DATETIME_FORMAT).date()
            now = datetime.now().date()

            while (date_index < now):
                demands_json = airbnb.listing_trip_demands(listing['id'], date_index)
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
                    Demand.update_or_create(self._db, **params)

                date_index = add_months(date_index)

    def threads(self):
        thread_index = 0
        while True:
            response = airbnb.threads(thread_index)
            total_threads = int(response['thread_count'])
            threads = response['threads']
            for t in threads:
                t = t['thread']
                params = {
                    'id': t['id'],
                    'user_id': self._user['id'],
                    'status': t['status'],
                    'unread': t['unread'],
                    'responded': t['responded'],
                    'other_user_id': t['other_user']['user']['id'],
                    'other_user_first_name': t['other_user']['user']['first_name'],
                    'preview': t['preview'],
                    'updated_at': t['updated_at']
                }
                Thread.update_or_create(self._db, **params)

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

             params = {
                'id': reservation['id'],
                'thread_id': reservation['thread_id'],
                'inquiry_checkin_date': thread['inquiry_checkin_date'],
                'inquiry_checkout_date': thread['inquiry_checkout_date'],
                'inquiry_number_of_guests': thread['inquiry_number_of_guests'],
                'inquiry_price_native': thread['inquiry_price_native'],
                'listing_id': listing['id'],
                'price': listing['price'],
                'guest_id': guest['id'],
                'currency': reservation['native_currency'],
                'instant_bookable': reservation['instant_bookable'],
                'is_superhost': host_user['is_superhost'],
                'identity_verified': guest['identity_verified'],
                'guest_created_at': guest['created_at'],
                'status': reservation['status']
             }

             ReservationRequest.update_or_create(self._db, **params)
