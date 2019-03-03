#!/usr/bin/python

from flask import request, jsonify
from sqlalchemy import create_engine
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from api_functions import query

import json
import sys

import post
from places import *

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

sanity_wo = list(get_sanity_offline_data())
for wo in sanity_wo:
    #Skip invalid addresses
    if not wo.good_addr:
        continue
    zone_id = post.getZone(conn, wo.zone) 
    location_id = post.getLocation(conn, wo.text_addr, wo)
    status_id = post.getStatus(conn, wo.status)
    reporter_id = post.getReporter(conn, wo.reporter) 
    priority_id = post.getPriority(conn, wo.priority)
    conn.execute("INSERT INTO reported(status_id, location_id, zone_id, reporter_id, priority_id) VALUES (%s, %s, %s, %s, %s)", (status_id, location_id, zone_id, reporter_id, priority_id,))
    currentReportedID = query("SELECT id FROM reported WHERE location_id=%s", location_id)[0]
    conn.execute("INSERT INTO workorders(request_id, w_o) VALUES (%s, %s)", (currentReportedID[0][0], wo.wo_num,))
