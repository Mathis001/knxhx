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
