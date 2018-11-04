"""
Create threads
"""

from yoyo import step

__depends__ = {'20170402_04_ZVAte-create-synclog'}

steps = [
    step(
        """CREATE TABLE threads (
                id                      integer NOT NULL PRIMARY KEY,
                user_id                 integer NOT NULL,
                status                  varchar(64) NOT NULL,
                unread                  boolean NOT NULL,
                other_user_id           integer NOT NULL,
                updated_at  timestamp without time zone default (now() at time zone 'utc'),
                created_at  timestamp without time zone default (now() at time zone 'utc'),

                CONSTRAINT fk_threads_user_id FOREIGN KEY (user_id)
                REFERENCES users (id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
        )""",
        "DROP TABLE threads")
]
