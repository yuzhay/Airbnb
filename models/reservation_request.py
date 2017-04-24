class ReservationRequest:

    @staticmethod
    def create(db, **params):
        request = (
                    "INSERT INTO reservation_requests "
                    "(id, thread_id, inquiry_checkin_date, inquiry_checkout_date,"
                    "inquiry_number_of_guests, inquiry_price_native, listing_id,"
                    "price, guest_id, currency, instant_bookable, is_superhost,"
                    "identity_verified, guest_created_at, status, pending_began_at, pending_expires_at) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    )
        return db.execute(
            request,
            (
                params['id'], params['thread_id'], params['inquiry_checkin_date'],
                params['inquiry_checkout_date'], params['inquiry_number_of_guests'],
                params['inquiry_price_native'], params['listing_id'],
                params['price'], params['guest_id'], params['currency'],
                params['instant_bookable'], params['is_superhost'],
                params['identity_verified'], params['guest_created_at'], params['status'],
                params['pending_began_at'], params['pending_expires_at']
            )
        )

    @staticmethod
    def update(db, **params):
        request = (
                    "UPDATE reservation_requests SET "
                        "thread_id = %s, inquiry_checkin_date = %s, inquiry_checkout_date = %s,"
                        "inquiry_number_of_guests = %s, inquiry_price_native = %s, listing_id = %s,"
                        "price = %s, guest_id = %s, currency = %s, instant_bookable = %s, is_superhost = %s,"
                        "identity_verified = %s, guest_created_at = %s, status = %s, "
                        "pending_began_at = %s, pending_expires_at = %s "
                    "WHERE id = %s"
                    )
        return db.execute(
            request,
            (
                params['thread_id'], params['inquiry_checkin_date'],
                params['inquiry_checkout_date'], params['inquiry_number_of_guests'],
                params['inquiry_price_native'], params['listing_id'],
                params['price'], params['guest_id'], params['currency'],
                params['instant_bookable'], params['is_superhost'],
                params['identity_verified'], params['guest_created_at'], params['status'],
                params['pending_began_at'], params['pending_expires_at'],
                params['id']
            )
        )

    @staticmethod
    def exists(db, id):
        result = db.execute("SELECT id FROM reservation_requests WHERE id = %s", [id])
        return result.rowcount > 0

    @staticmethod
    def update_or_create(db, **params):
        if ReservationRequest.exists(db, params['id']):
            ReservationRequest.update(db, **params)
        else:
            ReservationRequest.create(db, **params)
