#!/usr/bin/env python3

from common import *
from sync import Sync
from competitors import Competitors

sync = Sync(DB)
sync.run(date(2016,8,1))
# #
# sync.hosting_activities(date(2016,8,1))
# sync.host_earnings(date(2016,8,1))

competitors = Competitors(DB, COMPETITORS)
competitors.run()


# b = User2.update_or_create(db, **{'id': '10', 'first_name': 'YYYY', 'last_name': 'ZZZZ'})
# print(b)
#result = airbnb.host_earnings()
# result = airbnb.hosting_activities(year=2016, month=9)
#print(json.dumps(result, indent=2, sort_keys=True))

# c = User2.get(db, **{'id': 10})
# print(c)
