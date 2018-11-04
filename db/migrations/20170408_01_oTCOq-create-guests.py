"""
Create Guests
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """CREATE TABLE guests (
            id integer NOT NULL PRIMARY KEY,
            email varchar(255),
            first_name varchar(128),
            full_name varchar(255),
            phone varchar(32),
            region_code char(2),
            country varchar(64),
            updated_at  timestamp without time zone default (now() at time zone 'utc'),
            created_at  timestamp without time zone default (now() at time zone 'utc')
        )""",
        "DROP TABLE guests"
    )
]
