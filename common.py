from datetime import date
import configparser
import json
from airbnb import Api
from db import Db
from datetime import datetime, date, time, timedelta
import os
import requests

from models.listing import Listing
from models.demand import Demand
from models.user import User
from models.thread import Thread
from models.reservation_request import ReservationRequest
from models.hosting_activity import HostingActivity
from models.model import Model
from models.competitor import Competitor
from models.user2 import User2
from models.host_earning import HostEarning
from models.sync_log import SyncLog

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# Load config
CONFIG = configparser.ConfigParser()
CONFIG.read('config.ini')

# Connect to AirBnb API
AIRBNB = Api(CONFIG['airbnb']['login'], CONFIG['airbnb']['pass'])

COMPETITORS = CONFIG['competitors']['rooms'].split(',')

# Connect to database
DB = Db(CONFIG['database']['name'], CONFIG['database']['user'], CONFIG['database']['password'])

def add_months(sourcedate, months=1):
    """Add extra month to date"""
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    return date(year, month, 1)
