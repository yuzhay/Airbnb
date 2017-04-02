"""
Create Listings
"""

from yoyo import step

__depends__ = {'20170402_01_owjPI-create-users'}

steps = [
    step(
        """CREATE TABLE listings (
            id          integer NOT NULL PRIMARY KEY,
            name        varchar(255) NOT NULL,
            user_id     integer NOT NULL,
            updated_at  timestamp without time zone default (now() at time zone 'utc'),
            created_at  timestamp without time zone default (now() at time zone 'utc'),

            CONSTRAINT fk_listing_user_id FOREIGN KEY (user_id)
            REFERENCES users (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
        );""",
        "DROP TABLE listings")
]
