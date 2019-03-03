#!/usr/bin/python
from flask import jsonify
from datetime import date, datetime
from sqlalchemy import create_engine
from dateutil.relativedelta import relativedelta
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

# change _create type from string to datetime.date
def str_to_date(_date):
    if _date:
        try:
            _date = datetime.strptime(_date, '%Y-%m-%d')
            return _date
        except:
            pass

# performs MySQL query with select statement and any optional parameters
def query(select, option):
    conn = engine.connect()
    if option:
        query = conn.execute(select, option)
    else:
        query = conn.execute(select)
    conn.close()

    return [query.fetchall(), query.keys()]

# dictionary zips row headers and data into array of keyvalue pairs
def dictzip(row, headers):
    json_data=[]
    for result in row:
        json_data.append(dict(zip(headers,result)))
    return json_data

def getReporterFromId(_reporterid):
    return query("SELECT name FROM reporter WHERE id=%s", _reporterid)[0]

def getZoneFromId(_zoneid):
    return query("SELECT zone_number FROM zone WHERE id=%s", _zoneid)[0]

def getStatusFromId(_statusid):
    return query("SELECT name FROM status WHERE id=%s", _statusid)[0]

def getPriorityFromId(_priorityid):
    return query("SELECT name FROM priority WHERE id=%s", _priorityid)[0]

def getLocationFromId(_locationid):
    return query("SELECT full_address FROM location WHERE id=%s", _locationid)[0]
