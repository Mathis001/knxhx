#!/usr/bin/env python3
import json
import requests
import csv
import re
import datetime
import pickle

csvfile = './open_potholes.csv'
picklefile = './potholeworkoders.pickles'
sanity_picklefile = './sanity_potholes.pickles'
geocoding_api_key = 'AIzaSyDbZWg9g0t3QIuZAyz5azDuXUxx6vDV7fg'
maps_geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json'

class PotholeLocation:
    COUNTY_RE = re.compile('Knox County', re.IGNORECASE)
    STATE_RE = re.compile('TN', re.IGNORECASE)

    def __init__(self, place_id, lat, lng, format_addr, addr_comp):
        self.place_id = place_id
        self.lat = lat
        self.lng = lng
        self.format_addr = format_addr
        self.addr_comp = addr_comp

    @classmethod
    def make_latlng(cls, lat, lng):
        payload = {'latlng': '{},{}'.format(lat, lng),
                   'result_type': 'street_address',
                   'location_type': 'ROOFTOP',
                   'key': geocoding_api_key,
                  }
        goog_data = requests.get(maps_geocode_url, params=payload)
        data = goog_data.json()
        if data['status'] != 'OK':
            print('status is not OK: {}'.format(data['status']))
            return None
        if len(data['results']) < 1:
            print('got no results')
            return None
        result = data['results'][0]
        return cls(result['place_id'],
                   result['geometry']['location']['lat'],
                   result['geometry']['location']['lng'],
                   result['formatted_address'],
                   result['address_components'])

    @classmethod
    def make_addr(cls, address, append_loc):
        if append_loc is not None:
            address = '{}, {}'.format(address, append_loc)
        payload = {'address': address,
                   'region': 'us',
                   'result_type': 'street_address',
                   'location_type': 'ROOFTOP',
                   'key': geocoding_api_key,
                  }
        goog_data = requests.get(maps_geocode_url, params=payload)
        data = goog_data.json()
        if data['status'] != 'OK':
            print('status is not OK: {}'.format(data['status']))
            return None
        if len(data['results']) < 1:
            print('got no results')
            return None
        winning_result = None
        if len(data['results']) == 1:
            winning_result = data['results'][0]
        else:
            for res in data['results']:
                valid_loc = PotholeLocation.validate_loc_type(res)
                valid_cty = PotholeLocation.validate_county(res)
                if valid_loc and valid_cty:
                       winning_result = res
                       break
        if winning_result is None:
            print('no valid results')
            return None
        return cls(result['place_id'],
                result['geometry']['location']['lat'],
                result['geometry']['location']['lng'],
                result['formatted_address'],
                result['address_components'])

    @staticmethod
    def validate_loc_type(res):
        valid = True
        try:
            if res['geometry']['location_type'] != 'ROOFTOP':
                valid = False
        except KeyError:
            valid = False
        return valid

    @staticmethod
    def validate_county(res):
        valid = True
        try:
            county = res['address_components'][4]['long_name']
            state = res['address_components'][5]['short_name']
            if COUNTY_RE.match(county) is None:
                valid = False
            elif STATE_RE.match(state) is None:
                valid = False
        except KeyError:
            valid = False
        return valid



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

    def pretty_print(self):
        print('Workorder Number: {}'.format(self.wo_num))
        print('\tValid address:\t{}'.format(self.good_addr))
        print('\tPriority:\t{}'.format(self.priority))
        print('\tInput address:\t{}'.format(self.text_addr))
        try:
            print('\tFormatted addr:\t{}'.format(self.format_addr))
            print('\tLatitude:\t{}'.format(self.lat))
            print('\tLongitude:\t{}'.format(self.lng))
            print('\tPlace ID:\t{}'.format(self.place_id))
        except AttributeError:
            pass

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

def get_sanity_offline_data():
    with open(sanity_picklefile, 'rb') as spf:
        while True:
            try:
                yield pickle.load(spf)
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
                wo.lng = data['geometry']['location']['lng']
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

with open(sanity_picklefile, 'wb') as spf:
    for wo in priority_wo:
        pickle.dump(wo, spf)

sanity_wo = list(get_sanity_offline_data())

print('========================================================================')
for wo in sanity_wo:
    print('{}: {}'.format(wo.text_addr, wo.place_id))
print('========================================================================')
for wo in sanity_wo:
    wo.pretty_print()

testpl = PotholeLocation.make_latlng('35.9625505', '-83.9161831')
print(testpl.place_id)
print(testpl.lat)
print(testpl.lng)
print(testpl.format_addr)
print(testpl.addr_comp)

