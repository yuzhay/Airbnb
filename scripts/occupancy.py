import calendar
import json
from datetime import date, datetime, timedelta
from models import Reservation, Occupancy, Listing

class OccupancyCalculator:

  def __init__(self, db):
    self._db = db
    self.occupancy = {}
    self.counter = 0

    listings = Listing.get_all(self._db)
    for l in listings:
      self.occupancy[l.id] = {}



  def run(self):
    reservations = Reservation.get_where(self._db, '*', "user_facing_status_key='complete'")
    for r in reservations:
      index_date = r.start_date
      while(index_date < r.end_date):
        year = index_date.year
        month = index_date.month

        index_date += timedelta(1)
        self.__add(r.listing_id, year, month, 1)

    self.save()

  def __add(self, l_id, year, month, days):
    self.occupancy[l_id][year] = self.occupancy[l_id].get(year, {})
    self.occupancy[l_id][year][month] = self.occupancy[l_id][year].get(month, 0)
    self.occupancy[l_id][year][month] += days

    self.counter += days

  def __print(self, param):
    print(json.dumps(param, indent=2, sort_keys=True))
    print(self.counter)

  def save(self):
    for listing_id in self.occupancy:
      for year in self.occupancy[listing_id]:
        for month in self.occupancy[listing_id][year]:
          days = self.occupancy[listing_id][year][month]
          params = {
            'month': month,
            'year': year,
            'listing_id': listing_id,
            'days_in_month': calendar.monthrange(year,month)[1],
            'occupancy': days
          }
          Occupancy.update_or_create(self._db, params = params)
