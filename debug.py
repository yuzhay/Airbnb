#!/usr/bin/env python3

import configparser
import json
import pprint
from datetime import date, datetime, time, timedelta
from airbnb import Api


# Load config
CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

# Connect to AirBnb API
AIRBNB = Api(CONFIG['airbnb']['login'], CONFIG['airbnb']['pass'])

#pprint.pprint(AIRBNB.get_profile()['user'])
#pprint.pprint(AIRBNB.listings())


# pprint.pprint(AIRBNB.listing(19616566))

now = datetime.now().date()
pprint.pprint(AIRBNB.listing_trip_demands(19616566, now))
