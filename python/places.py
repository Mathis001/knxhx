#!/usr/bin/env python3
import json
import requests
import csv
import re
import datetime
import pickle

csvfile = './open_potholes.csv'
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
#        print('{} len {}'.format(address, len(data['results'])))
        winning_result = None
        if len(data['results']) == 1:
            res = data['results'][0]
            valid_loc = PotholeLocation.validate_loc_type(res)
#            print('{} validloc? {}'.format(address, valid_loc))
            valid_cty = PotholeLocation.validate_county(res)
#            print('{} validcty? {}'.format(address, valid_cty))
            if valid_loc and valid_cty:
                winning_result = res
        else:
            for res in data['results']:
                valid_loc = PotholeLocation.validate_loc_type(res)
                valid_cty = PotholeLocation.validate_county(res)
                if valid_loc and valid_cty:
                       winning_result = res
                       break
        if winning_result is None:
            print('no valid results for {}'.format(address))
            return None
        return cls(winning_result['place_id'],
                   winning_result['geometry']['location']['lat'],
                   winning_result['geometry']['location']['lng'],
                   winning_result['formatted_address'],
                   winning_result['address_components'])

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
            add_comp = res['address_components']
            cty_idx = PotholeLocation.find_county_idx(add_comp)
            st_idx = PotholeLocation.find_state_idx(add_comp)
            county = add_comp[cty_idx]['long_name']
            state = add_comp[st_idx]['short_name']
            if PotholeLocation.COUNTY_RE.match(county) is None:
#                print('invalid county: {}'.format(res['address_components']))
                valid = False
            elif PotholeLocation.STATE_RE.match(state) is None:
#                print('invalid state: {}'.format(res['address_components']))
                valid = False
        except KeyError:
#            print("key error: {}".format(res['address_components']))
            valid = False
        except IndexError:
#            print("index error: {}".format(res['address_components']))
            valid = False
        return valid

    @staticmethod
    def find_add_comp_idx(address_components, comp_name):
        index = None
        for idx, comp in enumerate(address_components):
            if comp_name in comp['types']:
                index = idx
        return index

    @staticmethod
    def find_county_idx(address_components):
        return PotholeLocation.find_add_comp_idx(address_components,
                'administrative_area_level_2')

    @staticmethod
    def find_state_idx(address_components):
        return PotholeLocation.find_add_comp_idx(address_components,
                'administrative_area_level_1')

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
        self.text_addr = loc_addr
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
        self.pot_loc = PotholeLocation.make_addr(self.text_addr,
                                                 self.city_text)
        if self.pot_loc is not None:
            self.good_addr = True
        else:
            self.good_addr = False

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
        if self.good_addr:
            print('\tFormatted addr:\t{}'.format(self.pot_loc.format_addr))
            print('\tLatitude:\t{}'.format(self.pot_loc.lat))
            print('\tLongitude:\t{}'.format(self.pot_loc.lng))
            print('\tPlace ID:\t{}'.format(self.pot_loc.place_id))
            print('\tAddr Comp:\t{}'.format(self.pot_loc.addr_comp))

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

    with open(sanity_picklefile, 'wb') as pf:
        for wo in priority_wo:
            pickle.dump(wo, pf)

def get_sanity_offline_data():
    with open(sanity_picklefile, 'rb') as spf:
        while True:
            try:
                yield pickle.load(spf)
            except EOFError:
                break

def get_address(lat, lng):
    location = PotholeLocation.make_latlng(lat, lng)
    return(location.format_addr, location.addr_comp[2]['short_name'])

def main():
    #get_online_data()

    sanity_wo = list(get_sanity_offline_data())

    #print('========================================================================')
    for wo in sanity_wo:
        wo.pretty_print()

    #testpl = PotholeLocation.make_latlng('35.9625505', '-83.9161831')
    #print(testpl.place_id)
    #print(testpl.lat)
    #print(testpl.lng)
    #print(testpl.format_addr)
    #print(testpl.addr_comp)

if __name__ == "__main__":
    main()
