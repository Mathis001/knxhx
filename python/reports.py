#!/usr/bin/python
from flask import jsonify
from api_functions import query
from post import post

def postReport():
    json_form = request.get_json(force=True)
    post(json_form)

def postLocationGPS():
    json_form = request.get_json(force=True)
    
def postLocationAddress():
    json_form = request.get_json(force=True)

def getAllReports():
    rv = query("SELECT * FROM `reported` ORDER BY `id`", '')[0]
    if rv:
        print(rv)
        return jsonify()
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404

def getAllWorkorders():
    pass

def putReportStatus(status):
    pass

def getLocationAddress(address):
    rv = query("SELECT `id`, `status_id`, ` FROM `reported` WHERE location_id=(SELECT * FROM `location` WHERE `street_name`=%s) ORDER BY `id`", location)[0]
    if rv:
        print(rv)
        return jsonify()
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404

def getLocationGPS(latitude, longitude):
    rv = query("SELECT `id`, `status_id`, ` FROM `reported` WHERE location_id=(SELECT * FROM `location` WHERE `street_name`=%s) ORDER BY `id`", location)[0]
    if rv:
        print(rv)
        return jsonify()
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404

def getJobsStatus(status):
    pass

def getNextJob(_id):
    pass

def getReportLocation(address):
    pass

def getWorkorderLocation(address):
    pass
