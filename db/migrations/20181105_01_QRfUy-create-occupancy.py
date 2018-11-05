"""
Create Occupancy
"""

from yoyo import step

__depends__ = {'20170402_02_QdyXy-create-listings'}

steps = [
    step(
        """CREATE TABLE occupancy (
            id              SERIAL NOT NULL PRIMARY KEY,
            listing_id      integer NOT NULL,
            month           integer NOT NULL,
            year            integer NOT NULL,
            days_in_month   integer NOT NULL,
            occupancy       integer NOT NULL,
            updated_at      timestamp without time zone default (now() at time zone 'utc'),
            created_at      timestamp without time zone default (now() at time zone 'utc'),

            UNIQUE(listing_id, year, month)
        );""",
        "DROP TABLE occupancy"
    )
]
