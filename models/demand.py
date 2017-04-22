class Demand:

    @staticmethod
    def create(db, **params):
        return db.execute(
            (
                "INSERT INTO demands "
                "(listing_id, booked, bookings, date, inquiries, page_views, unavailable) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s);"
            ),
            (
                params['listing_id'], params['booked'], params['bookings'],
                params['date'], params['inquiries'], params['page_views'], params['unavailable']
            )
        )

    @staticmethod
    def exists(db, listing_id, date):
        result = db.execute("SELECT id FROM demands WHERE listing_id = %s AND date = %s", (listing_id, date))
        return result.rowcount > 0

    @staticmethod
    def update(db, **params):
        return db.execute(
            (
                "UPDATE demands SET "
                    "booked = %s, bookings = %s, inquiries = %s, "
                    "page_views = %s, unavailable = %s "
                "WHERE listing_id = %s AND date = %s;"
            ),
            (
                params['booked'], params['bookings'], params['inquiries'],
                params['page_views'], params['unavailable'],
                params['listing_id'], params['date']
            )
        )

    @staticmethod
    def update_or_create(db, **params):
        if Demand.exists(db, params['listing_id'], params['date']):
            Demand.update(db, **params)
        else:
            Demand.create(db, **params)
