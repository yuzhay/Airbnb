"""
Create Demands
"""

from yoyo import step

__depends__ = {'20170402_02_QdyXy-create-listings'}

steps = [
    step(
        """CREATE TABLE demands (
                id          SERIAL NOT NULL PRIMARY KEY,
                listing_id  integer NOT NULL,
                date        date NOT NULL,
                booked      boolean NOT NULL,
                page_views  integer NOT NULL,
                inquiries   integer NOT NULL,
                bookings    integer NOT NULL,
                unavailable boolean NOT NULL,
                updated_at  timestamp without time zone default (now() at time zone 'utc'),
                created_at  timestamp without time zone default (now() at time zone 'utc'),

                CONSTRAINT fk_demands_listing_id FOREIGN KEY (listing_id)
                REFERENCES listings (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,

                UNIQUE (listing_id, date)
        )""",
        "DROP TABLE demands")
]
