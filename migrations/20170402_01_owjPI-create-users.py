"""
Create Users
"""

from yoyo import step

__depends__ = {}

steps = [
    step(
        """CREATE TABLE users (
            id          integer NOT NULL PRIMARY KEY,
            first_name  varchar(255) NOT NULL,
            last_name   varchar(255) NOT NULL,
            updated_at  timestamp without time zone default (now() at time zone 'utc'),
            created_at  timestamp without time zone default (now() at time zone 'utc')
        );""",
        "DROP TABLE users"
    )
]
