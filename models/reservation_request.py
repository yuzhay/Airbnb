class ReservationRequest:

    @staticmethod
    def create(
        db,
        id,
        thread_id,
        inquiry_checkin_date,
        inquiry_checkout_date,
        inquiry_number_of_guests,
        inquiry_price_native,
        listing_id,
        price,
        guest_id,
        currency,
        instant_bookable,
        is_superhost,
        identity_verified,
        guest_created_at,
        status):

        request = (
                    "INSERT INTO reservation_requests "
                    "(id, thread_id, inquiry_checkin_date, inquiry_checkout_date,"
                    "inquiry_number_of_guests, inquiry_price_native, listing_id,"
                    "price, guest_id, currency, instant_bookable, is_superhost,"
                    "identity_verified, guest_created_at, status) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    )
        return db.execute(
            request,
            (
                id, thread_id, inquiry_checkin_date, inquiry_checkout_date,
                inquiry_number_of_guests, inquiry_price_native, listing_id,
                price, guest_id, currency, instant_bookable, is_superhost,
                identity_verified, guest_created_at, status
            )
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM reservation_requests WHERE id = %s", [id])
        return result.rowcount > 0
