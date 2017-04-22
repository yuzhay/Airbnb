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

    @staticmethod
    def update(db, listing_id, booked, bookings, date, inquiries, page_views, unavailable):
        return db.execute(
            (
                "UPDATE demands SET "
                    "booked = %s, bookings = %s, inquiries = %s, "
                    "page_views = %s, unavailable = %s, user_id = %s "
                "WHERE listing_id = %s AND date = %s;"
            ),
            (booked, bookings, inquiries, page_views, unavailable, listing_id, date)
        )

    @staticmethod
    def update_or_create(db, listing_id, booked, bookings, date, inquiries, page_views, unavailable):
        if Demand.exists(db, listing_id, date):
            Demand.update(db, listing_id, booked, bookings, date, inquiries, page_views, unavailable)
        else:
            Demand.create(db, listing_id, booked, bookings, date, inquiries, page_views, unavailable)
