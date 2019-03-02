#!/usr/bin/python
from flask import jsonify
from api_functions import query

def post():
    pass

def put():
    pass

def get():
    rv = query("SELECT `id` FROM `reported` ORDER BY `id`")[0]
    if rv:
        return jsonify()
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404

def getLocation(location):
    rv = query("SELECT `id` FROM `reported` WHERE location=%s ORDER BY `id`", location)[0]
    if rv:
        return jsonify()
    else:
        return jsonify({'html':'<span>Error: No reports found</span>','text':'Error: No reports found', 'status':404}), 404
