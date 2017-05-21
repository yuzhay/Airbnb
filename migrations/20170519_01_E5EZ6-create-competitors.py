"""
Create Competitors
"""

from yoyo import step

__depends__ = {'20170429_01_Vax7m-create-hostearnings'}

steps = [
    step(
      """CREATE TABLE competitors(
          date          date NOT NULL,
          listing_id    integer NOT NULL,
          price         real NOT NULL,
          currency      varchar(16) NOT NULL,

          UNIQUE (date, listing_id)
      )""",
      "DROP TABLE competitors"
    )
]
