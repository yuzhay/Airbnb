class Demand:

    @staticmethod
    def create(db, listing_id, booked, bookings, date, inquiries, page_views, unavailable):
        return db.execute(
            "INSERT INTO demands (listing_id, booked, bookings, date, inquiries, page_views, unavailable) VALUES (%s, %s, %s, %s, %s, %s, %s);",
            (listing_id, booked, bookings, date, inquiries, page_views, unavailable)
        )

    @staticmethod
    def exists(db, listing_id, date):
        result = db.execute("SELECT id FROM demands WHERE listing_id = %s AND date = %s", (listing_id, date))
        return result.rowcount > 0
