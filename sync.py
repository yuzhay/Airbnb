#!/usr/bin/env python3

from common import *
import time

class Sync:
    """Full synchronizer"""

    _db = None
    _user = None
    _listings = None
    _timer = None

    def __init__(self, db):
        """Constructor"""
        self._db = db
        self._timer = time.time()

    def console(self, msg):
        """Print console"""
        print("[{0:0.2f}]\t{1}".format(time.time() - self._timer, msg))

    def json_print(self, param):
        print(json.dumps(param, indent=2, sort_keys=True))

    def run(self, date=date(2016, 8, 1)):
        """Run synchronization"""
        SyncLog.start(self._db)
        self.console("Syncing started")

        self.users()
        self.console("Users syncronized")

        self.listings(date)
        self.console("Listings syncronized")

        self.threads()
        self.console("Threads syncronized")

        self.reservation_requests()
        self.console("ReservationRequests syncronized")

        self.hosting_activities(date)
        self.console("HostingActivities syncronized")

        self.host_earnings(date)
        self.console("HostEarnings syncronized")

        self.console("Syncing finished")
        SyncLog.finish(self._db)

    def users(self):
        """Sync users"""
        self._user = AIRBNB.get_profile()['user']
        params = {key: self._user[key] for key in ['id', 'first_name', 'last_name']}
        User.update_or_create(self._db, params)

    def listings(self, start_date):
        """Sync listings"""
        self._listings = AIRBNB.listings()['listings']
        for listing in self._listings:
            params = {
                'id': listing['id'],
                'name': listing['name'],
                'user_id': self._user['id']
            }
            Listing.update_or_create(self._db, params)

            # start_date = datetime.strptime(self._user['created_at'], DATETIME_FORMAT).date()
            now = datetime.now().date()
            date_index = start_date

            while (date_index < now):
                demands_json = AIRBNB.listing_trip_demands(listing['id'], date_index)
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
        """Sync Threads"""
        thread_index = 0
        while True:
            response = AIRBNB.threads(thread_index)
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
                Thread.update_or_create(self._db, params)

            thread_index += len(threads)
            if thread_index >= total_threads:
                break

    def reservation_requests(self):
        """Sync Reservation Requests"""
        self._threads = Thread.get_all(self._db)
        for thread in self._threads:
            response = AIRBNB.reservation_requests(thread[0])
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
                'status': reservation['status'],
                'pending_began_at': reservation['pending_began_at'],
                'pending_expires_at': reservation['pending_expires_at']
            }

            ReservationRequest.update_or_create(self._db, params)

    def hosting_activities(self, start_date):
        """Sync HostingActivities"""
        date_index = start_date

        while date_index < add_months(datetime.now(), 3):
            params = {
                'year': date_index.year,
                'month': date_index.month
            }
            ha = AIRBNB.hosting_activities(**params)['hosting_activities'][0]

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

    def host_earnings(self, start_date):
        """Sync HostEarnings"""
        date_index = start_date

        while date_index < add_months(datetime.now(), 3):
            params = {
                'year': date_index.year,
                'month': date_index.month
            }
            he = AIRBNB.host_earnings(**params)['host_earnings'][0]

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
