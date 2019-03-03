#!/usr/bin/python
from flask import request, jsonify
from api_functions import *
from sqlalchemy import create_engine
import post
import json
from places import get_address
from routing import split_list_half, get_optimized_route

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

def postReport():
    json_form = request.get_json(force=True)
    post.post(json_form)

def postLocationGPS():
    json_form = request.get_json(force=True)
    latitude = json_form['latitude']
    longitude = json_form['longitude']
    address = get_address(latitude, longitude)
    full_address = address[0]
    city = address[1]

    conn.execute("INSERT INTO location(input_address, full_address, city, latitude, longitude) VALUES (%s,%s,%s,%s,%s)", (full_address, full_address, city, latitude, longitude))
    currentLocationID = query("SELECT id FROM location WHERE full_address=%s", address)[0]
    if currentLocationID[0][0]:
        return jsonify({'html':'<span>Location Created</span>','text':'Location created at '+currentLocationID[0][0], 'status':200}), 200
    else:
        return jsonify({'html':'<span>Error: Location unable to be added</span>','text':'Error: Location unable to be added', 'status':404}), 404
    
def postLocationAddress():
    json_form = request.get_json(force=True)

    address = json_form['address']
    wo = PotholeWorkorder(organ=None,
                         loc_addr=address,
                         status=None,
                         req_num=None,
                         zone=None,
                         reporter=None,
                         priority=None)
    location_id = post.getLocation(conn, address, wo)
    return jsonify({'html':'<span>Location Created</span>','text':'Location created at '+location_id, 'status':200}), 200

def getAllReports():
    rv = query("SELECT * FROM `reported` ORDER BY `id`", '')[0]
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404

def getAllWorkorders():
    rv = query("SELECT * FROM `workorders` ORDER BY `id`", '')[0]
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404

#Add to yaml
def putReportStatus(_id, status):
    json_form = request.get_json(force=True)

    _id = json_form['id']
    _status = json_form['status']
    
    status_id = post.getStatus(conn, _status)
    rv = conn.execute("UPDATE reports SET status_id=%s WHERE id=%s", (_status, _id))
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: Could not update report status. Report not found.</span>','text':'Error: Could not update report status. Report not found.', 'status':404}), 404

#def getLocationAddress(address):
    #rv = query("SELECT `id` FROM `location` WHERE input_address=%s", address)[0]
    #if rv:
        #print(rv)
        #return jsonify(dictzip(rv[0], rv[1]))
    #else:
        #return jsonify({'html':'<span>Error: No location found with that address</span>','text':'Error: No location found with that address', 'status':404}), 404

def getLocationGPS(latitude, longitude):
    rv = query("SELECT `id` FROM `location` WHERE latitude=%s and longitude=%s", (latitude, longitude))[0]
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: No locations found with those coordinates</span>','text':'Error: No locations found with those coordinates', 'status':404}), 404

def getReportStatus(status):
    status_id = post.getStatus(conn, _status)
    rv = query("SELECT `id` from `reports` WHERE status_id=%s", status_id)[0]
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: No reports found with that status</span>','text':'Error: No reports found with that status', 'status':404}), 404

def getWorkorderStatus(status):
    status_id = post.getStatus(conn, _status)
    rv = query("SELECT `id` from `workorders` WHERE report_id=(SELECT `id` from `reports` WHERE status_id=%s)", status_id)[0]
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: No work orders found with that status</span>','text':'Error: No work orders found with that status', 'status':404}), 404

#Add to yaml
def getJobsByTruck(truck):
    pass

def create_workorder_from_id(_id):
    rv = query("SELECT `request_id`, `w_o` FROM `workorders` WHERE id=%s", _id)[0]
    if rv:
        print(rv)
        rv2 = query("SELECT * FROM `reported` WHERE id=%s", rv[0][0])[0]
        print(rv2)
        zone = getZoneFromId(rv2[0][0])
        status = getStatusFromId(rv2[0][0])
        address = getLocationFromId(rv2[0][0])
        priority = getPriorityFromId(rv2[0][0])
        reporter = getReporterFromId(rv2[0][0])
        return PotholeWorkorder('1/1/2001', 'organ', address, status, rv[1], 'req', zone, reporter, priority)
    else:
        pass

def get_valid_workorders(ids):
    wo_list = []
    for _id in ids:
        create_workorder_from_id(_id)
    return wo_list

#Assumes one truck
def getOptimalJobs():
    rv = query("SELECT `id` FROM `workorders`")[0]
    if rv:
        wo_list = get_workorders(rv[0])
        depot = PotholeWorkorder('1/1/2000', 'bob', '205 W Baxter Ave', 'status', 'num', 'req', 'zone', 'reporter', 0)
        (route1, route2) = split_list_half(rv)
        route1.insert(0, depot)
        route1.insert(len(route1), depot)
        route2.insert(0, depot)
        route2.insert(len(route2), depot)
        opt_route = get_optimized_route(route1)
        ids = []
        for wo in route1:
            rv = query("SELECT `id` FROM `workorders` WHERE w_o=%s", wo.wo_num)[0]
            ids.append(rv[0][0])
        return jsonify(get_workorders(rv[0]))
    else:
        return jsonify({'html':'<span>Error: No work orders found</span>','text':'Error: No work orders found', 'status':404}), 404

def getReportLocation(address):
    wo = PotholeWorkorder(organ=None,
                         loc_addr=address,
                         status=None,
                         req_num=None,
                         zone=None,
                         reporter=None,
                         priority=None)
    location_id = post.getLocation(conn, address, wo)
    rv = query("SELECT `id` from `reports` WHERE location_id=%s", location_id)[0]
    if rv:
        print(rv)
        return jsonify(dictzip(rv[0], rv[1]))
    else:
        return jsonify({'html':'<span>Error: No reports found with that address</span>','text':'Error: No reports found with that address', 'status':404}), 404

def getWorkorderLocation(address):
    wo = PotholeWorkorder(organ=None,
                         loc_addr=address,
                         status=None,
                         req_num=None,
                         zone=None,
                         reporter=None,
                         priority=None)
    location_id = post.getLocation(conn, address, wo)
    rv = query("SELECT `id` from `workorders` WHERE report_id=(SELECT `id` from `reports` WHERE location_id=%s)", location_id)[0]
    if rv:
        print(rv)
        return jsonify(create_workorder_from_id(rv[0][0]))
    else:
        return jsonify({'html':'<span>Error: No work orders found with that address</span>','text':'Error: No work orders found with that address', 'status':404}), 404
