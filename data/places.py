#!/usr/bin/env python3
import json
import requests
import csv
import re
import datetime
import pickle

csvfile = './open_potholes.csv'
picklefile = './potholeworkoders.pickles'
geocoding_api_key = 'AIzaSyDbZWg9g0t3QIuZAyz5azDuXUxx6vDV7fg'
maps_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'

class PotholeWorkorder:
    date_re = re.compile('(\d+)/(\d+)/(\d+)')
    city_text = 'knoxville, tn'

    def __init__(self, wo_date, organ, loc_addr, status,
            wo_num, req_num, zone, reporter, priority):
        wo_date_match = self.date_re.match(wo_date)
        self.wo_date = datetime.date(int(wo_date_match.group(3)),
                                     int(wo_date_match.group(1)),
                                     int(wo_date_match.group(2)))
        self.organ = organ
        self.text_addr = "{}, {}".format(loc_addr, self.city_text)
        self.status = status
        self.wo_num = wo_num
        self.req_num = req_num
        self.zone = zone
        self.reporter = reporter
        self.priority = priority

    def get_geocode(self):
        payload = {'address': self.text_addr,
                   'region': 'us',
                   'key': geocoding_api_key,
                   }
        self.goog_data = requests.get(maps_geocode_url, params=payload)
        self.data = self.goog_data.json()

def get_online_data():
    priority_wo = []
    with open(csvfile, 'r') as op:
        rdr = csv.reader(op)
        data_pri = 0 # use 0 as high priority
        for row in rdr:
            if PotholeWorkorder.date_re.match(row[0]) is not None:
                pw = PotholeWorkorder(row[0], #date
                                      row[1], #organ
                                      row[2], #addr
                                      row[3], #status
                                      row[4], #wo_num
                                      row[5], #req_num
                                      row[6], #zone
                                      row[7], #reporter
                                      data_pri
                                     )
                priority_wo.append(pw)

    for wo in priority_wo:
        wo.get_geocode()

    with open(picklefile, 'wb') as pf:
        for wo in priority_wo:
            pickle.dump(wo, pf)

def get_offline_data():
    with open(picklefile, 'rb') as pf:
        while True:
            try:
                yield pickle.load(pf)
            except EOFError:
                break

#get_online_data()

priority_wo = list(get_offline_data())

for wo in priority_wo:
    print(wo.data)


