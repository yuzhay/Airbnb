#!/usr/bin/env python3

import configparser
import yaml
import json
import os
import sys

from datetime import date

import requests
from airbnb import Api
from db import Database
from scripts import Sync
import pprint

# Load config
with open("config/config.yml", "r") as config:
  CONFIG = yaml.load(config)

# Connect to AirBnb API
AIRBNB = Api(CONFIG['airbnb']['user']['login'], CONFIG['airbnb']['user']['pass'])

# Connect to database
CONNECTION_STRING = "postgresql://{0}:{1}@localhost/{2} ./db/migrations".format(
    CONFIG['database']['user'],
    CONFIG['database']['password'],
    CONFIG['database']['name']
)
DB = Database(CONFIG['database']['name'], CONFIG['database']['user'], CONFIG['database']['password'])

if len(sys.argv) <= 1:
  print("See usage")
  exit(1)

command = sys.argv[1]
if command == "sync":
  sync = Sync(DB, AIRBNB, CONFIG['airbnb']['listings'])

  force = (len(sys.argv) > 2 and sys.argv[2] == '--force')
  sync.run(force)

elif command == 'migrate':
  os.system("yoyo apply --batch --database {0}".format(CONNECTION_STRING))
elif command == "rollback":
  os.system("yoyo rollback --batch --database {0}".format(CONNECTION_STRING))
else:
  print("Unknown command")
