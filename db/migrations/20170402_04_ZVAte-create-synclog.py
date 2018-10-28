"""
Create SyncLog
"""

from yoyo import step

__depends__ = {'20170402_03_pSemG-create-demands'}

steps = [
    step(
        """CREATE TABLE sync_log (
            id          SERIAL NOT NULL PRIMARY KEY,
            started_at  timestamp without time zone default (now() at time zone 'utc'),
            ended_at    timestamp without time zone default NULL
        )""",
        "DROP TABLE sync_log"
    )
]
