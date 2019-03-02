#!/usr/bin/python
from flask import request, jsonify
from sqlalchemy import create_engine
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from api_functions import query

import json
import sys
sys.path.insert(0, '../data/places')
import places

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

def readJSON(name, default, json_form):
    # Read in optional data, or set default values
    if name in json_form:
        result = json_form[name]
    else:
        result = default
    return result

def post():
    json_form = request.get_json(force=True)

    _date = json_form["date"]
    _organ = json_form["organ"]
    _location = json_form["location"]
    _status = json_form["status"]
    _workorder = json_form["workorder"]
    _req = json_form["req"]
    _zone = json_form["zone"]
    _caller = json_form["caller"]
    _priority = json_form["caller"]

    order = places.PotholeWorkorder(organ=_organ
                                    loc_addr=_location
                                    status=_status
                                    wo_num=_workorder
                                    req_num=_req
                                    zone=_zone
                                    reporter=_caller
                                    priority=_priority)
    #conn.execute(INSERT INTO 'workorders'
