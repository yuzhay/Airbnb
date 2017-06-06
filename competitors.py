from common import *

class Competitors(object):
    """Competitors synchronizer"""

    def __init__(self, db, rooms):
        self._db = db
        self._rooms = rooms

    def run(self, day=date.today()):
        """Retirieve and save competitors prices"""
        for room_id in self._rooms:
            listing = AIRBNB.listing(room_id)['listing']
            params = {
                'date': day,
                'room_id': room_id,
                'price': listing['price_native'],
                'currency': listing['listing_native_currency'],
                'data': json.dumps(listing)
            }
            Competitor.update_or_create(self._db, params)
