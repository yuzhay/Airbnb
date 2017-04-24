"""
Create ReservationRequests
"""

from yoyo import step

__depends__ = {'20170409_01_nINMY-create-threads'}

steps = [
    step("""
        CREATE TABLE reservation_requests (
            id                          integer NOT NULL PRIMARY KEY,
            thread_id                   integer NOT NULL,
            inquiry_checkin_date        date NOT NULL,
            inquiry_checkout_date       date NOT NULL,
            inquiry_number_of_guests    integer NOT NULL,
            inquiry_price_native        real NOT NULL,
            listing_id                  integer NOT NULL,
            price                       real NOT NULL,
            guest_id                     integer NOT NULL,
            currency                    varchar(16) NOT NULL,
            instant_bookable            boolean NOT NULL,
            is_superhost                boolean NOT NULL,
            identity_verified           boolean NOT NULL,
            guest_created_at            date NOT NULL,
            status                      varchar(16) NOT NULL,
            pending_began_at            date NOT NULL,
            pending_expires_at          date NOT NULL,

            updated_at  timestamp without time zone default (now() at time zone 'utc'),
            created_at  timestamp without time zone default (now() at time zone 'utc'),

            CONSTRAINT fk_reservation_requests_thread_id FOREIGN KEY (thread_id)
            REFERENCES threads (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,

            CONSTRAINT fk_reservation_requests_listing_id FOREIGN KEY (listing_id)
            REFERENCES listings (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
    )""",
    "DROP TABLE reservation_requests"
    )
]
