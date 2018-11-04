"""
Create HostActivities
"""

from yoyo import step

__depends__ = {'20170410_01_iCTAr-create-reservations'}

steps = [
    step(
        """ CREATE TABLE hosting_activities (
            year                integer NOT NULL,
            month               integer NOT NULL,
            nights_booked       integer NOT NULL,
            nights_unbooked     integer,
            occupancy_rate      integer,
            nights_price_min    integer NULL,
            nights_price_max    integer NULL,
            cleaning_fees       integer NOT NULL,

            updated_at  timestamp without time zone default (now() at time zone 'utc'),
            created_at  timestamp without time zone default (now() at time zone 'utc'),

            UNIQUE (year, month)
        );""",
        "DROP TABLE hosting_activities"
    )
]
