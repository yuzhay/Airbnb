from datetime import date
import configparser
from airbnb import Api
from db import Db
from datetime import datetime, date, time, timedelta
import os
import requests
import json

from models.listing import Listing
from models.demand import Demand
from models.user import User
from models.thread import Thread
from models.sync_log import SyncLog

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# Load config
config = configparser.ConfigParser()
config.read('config.ini')

# Connect to AirBnb API
airbnb = Api(config['airbnb']['login'], config['airbnb']['pass'])

# Connect to database
db = Db(config['database']['name'], config['database']['user'], config['database']['password'])

def add_months(sourcedate, months = 1):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12 )
    month = month % 12 + 1
    return date(year,month,1)
