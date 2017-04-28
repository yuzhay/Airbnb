#!/usr/bin/env python3

from common import *
from sync import Sync

sync = Sync(db)
#
#sync.hosting_activities(date(2016,8,1))

Model.create(db, **{'k_a': 'v_a', 'k_b': 'v_b'})

# result = airbnb.host_earnings(year=2016, month=9)
# result = airbnb.hosting_activities(year=2016, month=9)
#print(json.dumps(result, indent=2, sort_keys=True))
