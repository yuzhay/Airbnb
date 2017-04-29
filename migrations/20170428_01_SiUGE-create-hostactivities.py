"""
Create HostActivities
"""

from yoyo import step

__depends__ = {'20170410_01_iCTAr-create-reservationrequests'}

steps = [
    step(
        """ CREATE TABLE hosting_activities (
            year                integer NOT NULL,
            month               integer NOT NULL,
            nights_booked       integer NOT NULL,
            nights_unbooked     integer NOT NULL,
            occupancy_rate      integer NOT NULL,
            nights_price_min    integer NULL,
            nights_price_max    integer NULL,
            cleaning_fees       integer NOT NULL,

            UNIQUE (year, month)
        );""",
        "DROP TABLE hosting_activities"
    )
]
