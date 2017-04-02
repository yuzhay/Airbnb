#!/usr/bin/env python3

from common import *

#print(json.dumps(p, indent=2, sort_keys=True))

SyncLog.start(db)

user = airbnb.get_profile()['user']

if not User.exists(db, user['id']):
    User.create(db, user['id'], user['first_name'], user['last_name'])

listings = airbnb.listings()['listings']

for listing in listings:
    if not Listing.exists(db, listing['id']):
        Listing.create(db, listing['id'], listing['name'], user['id'])

    start_date = datetime.strptime(user['created_at'], DATETIME_FORMAT).date()
    now = datetime.now().date()

    date_index = date(2016,8,1)

    while (date_index < now):
        demands_json = airbnb.listing_trip_demands(listing['id'], date_index)
        demands = demands_json['listing_trip_demand']['monthly_trip_demand_counts'][0]['daily_trip_demand_counts']

        for demand in demands:
            if not Demand.exists(db, listing['id'], demand['date']):
                Demand.create(db, listing['id'], demand['booked'], demand['bookings'], demand['date'], demand['inquiries'], demand['page_views'], demand['unavailable'])

        date_index = add_months(date_index)

SyncLog.finish(db)
