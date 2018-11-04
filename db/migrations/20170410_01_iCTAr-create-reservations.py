"""
Create Reservations
"""

from yoyo import step

__depends__ = {'20170409_01_nINMY-create-threads'}

steps = [
    step("""
        CREATE TABLE reservations (
            confirmation_code           varchar(16) NOT NULL PRIMARY KEY,
            thread_id                   integer NOT NULL,
            start_date                  date NOT NULL,
            end_date                    date NOT NULL,
            booked_date                 date,
            earnings                    real NOT NULL,
            nights                      integer NOT NULL,
            host_vat_invoices           jsonb NOT NULL,
            guest_id                    integer NOT NULL,
            listing_id                  integer NOT NULL,
            updated_at  timestamp without time zone default (now() at time zone 'utc'),
            created_at  timestamp without time zone default (now() at time zone 'utc'),

            CONSTRAINT fk_reservations_thread_id FOREIGN KEY (thread_id)
            REFERENCES threads (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,

            CONSTRAINT fk_reservation_listing_id FOREIGN KEY (listing_id)
            REFERENCES listings (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
    )""",
    "DROP TABLE reservations"
    )
]
