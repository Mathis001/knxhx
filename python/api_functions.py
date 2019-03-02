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

def select(selection, json_data):
    # selection [<json tuple name>, <query>, <formater>, <optional system id>]
    # adds join table information to json_data object [serials, orders, features, hw/sw contracts, and add_hardware]
    for select in selection:

        if select[2] == "configTuple":
            for pair in query(select[1], '')[0]:
                json_data[select[0]] = [dict(zip(('id','name','active'),pair)) for pair in query(select[1], '')[0]]

        if select[2] == "configTriple":
            for pair in query(select[1], '')[0]:
                json_data[select[0]] = [dict(zip(('id','name','hardware_id','active'),pair)) for pair in query(select[1], '')[0]]

        if select[2] == "configList":
            json_data[select[0]] = [dict(zip(('id','active'),pair)) for pair in query(select[1], '')[0]]

        if select[2] == "systemList":
            for i in range(len(json_data)):
                rv = query(select[1], json_data[i]['master_id'])[0]
                items = []
                for item in rv:
                    items += item
                json_data[i][select[0]] = items

        if select[2] == "serialList":
            for i in range(len(json_data)):
                rv = query(select[1], (json_data[i]['master_id'], select[0],))[0]
                items = []
                if rv:
                    for item in rv:
                        items += item
                    json_data[i][select[0]] = items

        if select[2] == "orderList":
            for i in range(len(json_data)):
                rv = query(select[1], select[3])[0]
                items = []
                for item in rv:
                    items += item
                json_data[i][select[0]] = items

        if select[2] == "employeeTuple":
            for pair in query(select[1], '')[0]:
                json_data[select[0]] = [dict(zip(('id','login','name','tn_auth','department'),pair)) for pair in query(select[1], '')[0]]
    return json_data
