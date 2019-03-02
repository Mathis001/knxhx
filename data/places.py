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
        self.good_addr = None
        self.place_id = None
        self.lat = None
        self.lng = None
        self.format_addr = None
        self.addr_comp = None

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

def get_county(address_components):
    county = None
    state = None
    try:
        for area in address_components:
            if 'administrative_area_level_2' in area['types']:
                county = area['long_name']
            if 'administrative_area_level_1' in area['types']:
                state = area['short_name']
    except KeyError:
        pass
    if state is None or re.match('TN', state, re.IGNORECASE) is None:
        county = None
    return county

def check_county(address_components, valid_county):
    my_county = get_county(address_components)
    if my_county is not None and my_county.lower() == valid_county.lower():
        return True
    else:
        return False

def sanitize_locs(wos):
    for wo in wos:
#        for res in wo.data['results']:
#            print(res.keys())
#            print(res['geometry']['location_type'])
#            print('{}: '.format(wo.text_addr), end='')
#            if 'partial_match' in res.keys():
#                print(res['partial_match'])
#            else:
#                print('no')
        if len(wo.data['results']) == 1:
            data = wo.data['results'].pop()
            is_partial = 'partial_match' in data.keys()
            is_rooftop = data['geometry']['location_type'] == 'ROOFTOP'
            is_good_county = check_county(data['address_components'],
                    'Knox County')
            if is_partial or not is_good_county or not is_rooftop:
                wo.good_addr = False
                wo.place_id = None
                print('bad match for address {}'.format(wo.text_addr))
            else:
                wo.good_addr = True
                wo.place_id = data['place_id']
                wo.lat = data['geometry']['location']['lat']
                wo.lat = data['geometry']['location']['lng']
                wo.format_addr = data['formatted_address']
                wo.addr_comp = data['address_components']
        elif len(wo.data['results']) > 1:
            valid_res = None
            for res in wo.data['results']:
                if 'partial_match' in res.keys():
                    next
                if res['geometry']['location_type'] != 'ROOFTOP':
                    next
                county = get_county(res['address_components'])
                if check_county(res['address_components'], 'Knox County'):
                    if valid_res is None:
                        valid_res = res
                    else:
                        pass # TODO: only get first valid result for now?
            if valid_res is None:
                wo.good_addr = False
                wo.place_id = None
                print('bad match for address {}'.format(wo.text_addr))
            else:
                wo.good_addr = True
                wo.data = {'results': valid_res}
                wo.place_id = valid_res['place_id']
                wo.lat = data['geometry']['location']['lat']
                wo.lat = data['geometry']['location']['lng']
                wo.format_addr = data['formatted_address']
                wo.addr_comp = data['address_components']

#get_online_data()

priority_wo = list(get_offline_data())

sanitize_locs(priority_wo)
print('========================================================================')
for wo in priority_wo:
    print('{}: {}'.format(wo.text_addr, wo.place_id))
print('========================================================================')
for wo in priority_wo:
    print(wo)
