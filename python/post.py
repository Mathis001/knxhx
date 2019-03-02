#!/usr/bin/python
from flask import request, jsonify
from sqlalchemy import create_engine
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

import sys
sys.path.insert(0, './licenselib')
from licenselib import license
from api_functions import query

import json

# load configuration
with open('../config.json') as json_data_file:
    data = json.load(json_data_file)
    db_conn = data["mysql"]["connector"]
    db_host = data["mysql"]["hostname"]
    db_port = data["mysql"]["port"]
    db_user = data["mysql"]["username"]
    db_pass = data["mysql"]["password"]
    db_name = data["mysql"]["database"]

engine = create_engine('%s://%s:%s@%s:%s/%s' % (db_conn, db_user, db_pass, db_host, db_port, db_name), pool_pre_ping=True)
conn = engine.connect()


