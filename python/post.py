#!/usr/bin/python
from flask import request, jsonify
from sqlalchemy import create_engine
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from api_functions import query

import json
import sys
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

def readJSON(name, default, json_form):
    # Read in optional data, or set default values
    if name in json_form:
        result = json_form[name]
    else:
        result = default
    return result

def getReporter(conn, _reporter):
    currentReporterID = query("SELECT id FROM reporter WHERE name=%s", _reporter)[0]
    if not currentReporterID:
        conn.execute("INSERT INTO reporter(name, phone_number) VALUES (%s, %s)", (_reporter,"",))
        currentReporterID = query("SELECT id FROM reporter WHERE name=%s", _reporter)[0]
        return currentReporterID[0][0]
    else:
        return currentReporterID[0][0]

def getZone(conn, _zone):
    if not _zone:
        _zone = '0'
    currentZoneID = query("SELECT id FROM zone WHERE zone_number=%s", _zone)[0]
    if not currentZoneID:
        conn.execute("INSERT INTO zone(zone_number, zone_notes) VALUES (%s, %s)", (_zone,"",))
        currentZoneID = query("SELECT id FROM zone WHERE zone_number=%s", _zone)[0]
        return currentZoneID[0][0]
    else:
        return currentZoneID[0][0]

def getPriority(conn, _priority):
    if not _priority:
        _priority = 'Default'
    currentPriorityID = query("SELECT id FROM priority where name=%s", (_priority,))[0]
    if not currentPriorityID:
        conn.execute("INSERT INTO priority(name) VALUES (%s)", (_priority,))
        currentPriorityID = query("SELECT id FROM priority WHERE name=%s", (_priority,))[0]
        return currentPriorityID[0][0]
    else:
        return currentPriorityID[0][0]

def getStatus(conn, _status):
    currentStatusID = query("SELECT id FROM status where name=%s", _status)[0]
    if not currentStatusID:
        conn.execute("INSERT INTO status(name) VALUES (%s)", (_status,))
        currentStatusID = query("SELECT id FROM status WHERE name=%s", _status)[0]
        return currentStatusID[0][0]
    else:
        return currentStatusID[0][0]

def getLocation(conn, _location, wo):
    currentLocationID = query("SELECT id FROM location WHERE full_address=%s", wo.pot_loc.format_addr)[0]
    if not currentLocationID:
        conn.execute("INSERT INTO location(input_address, full_address, city, latitude, longitude) VALUES (%s,%s,%s,%s,%s)", (wo.text_addr, wo.pot_loc.format_addr, wo.pot_loc.addr_comp[2]['short_name'], wo.lat, wo.lng))
        currentLocationID = query("SELECT id FROM location WHERE full_address=%s", wo.pot_loc.format_addr)[0]
        return currentLocationID[0][0]
    else:
        return currentLocationID[0][0]


def post(json_form):
    _date = json_form["date"]
    _organ = json_form["organ"]
    _location = json_form["location"]
    _status = json_form["status"]
    _workorder = json_form["workorder"]
    _req = json_form["req"]
    _zone = json_form["zone"]
    _reporter = json_form["reporter"]
    _priority = readJSON("priority", "", json_form)

    wo = PotholeWorkorder(organ=_organ,
                                    loc_addr=_location,
                                    status=_status,
                                    wo_num=_workorder,
                                    req_num=_req,
                                    zone=_zone,
                                    reporter=_reporter,
                                    priority=_priority)

    zone_id = getZone(conn, _zone)
    location_id = getLocation(conn, _location, wo)  
    status_id = getStatus(conn, _status)
    reporter_id = getReporter(conn, _reporter)
    
    #Currently only 'Default'
    priority_id = getPriority(conn, _priority)

    conn.execute("INSERT INTO reported(status_id, location_id, zone_id, reporter_id, priority_id) VALUES (%s, %s, %s, %s, %s)", (status_id, location_id, zone_id, reporter_id, priority_id,))
    currentReportedID = query("SELECT id FROM reported WHERE location_id=%s", _location_id)[0]
    conn.execute("INSERT INTO workorders(request_id, w_o) VALUES (%s, %s)", (currentReportedID[0][0], wo.wo_num,))
