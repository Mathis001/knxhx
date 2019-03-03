#!/usr/bin/env python3
import json
import requests
import re
import pickle
from places import PotholeLocation
from places import PotholeWorkorder
from itertools import combinations
import math

sane_picklefile = './sanity_potholes.pickles'
directions_api_key = 'AIzaSyDbZWg9g0t3QIuZAyz5azDuXUxx6vDV7fg'
dir_url = 'https://maps.googleapis.com/maps/api/directions/json'
depot_addr = '205 W Baxter Ave, Knoxville, TN 37917'
MAX_WAYPOINTS = 23

def get_sanity_offline_data():
    with open(sane_picklefile, 'rb') as spf:
        while True:
            try:
                yield pickle.load(spf)
            except EOFError:
                break

#depot = PotholeLocation.make_addr(depot_addr)
depot = PotholeWorkorder('1/1/2000', 'bob', '205 W Baxter Ave', 'status', 'num', 'req', 'zone', 'reporter', 0)

sanity_wo = list(get_sanity_offline_data())

def get_valid_workorders(workorders):
    valid_wo = []
    for wo in workorders:
        if wo.good_addr:
            valid_wo.append(wo)
    return valid_wo

def get_ll_tuples(workorders):
    ll_tups = []
    for wo in workorders:
        ll_tups.append((wo.pot_loc.lat, wo.pot_loc.lng))
    return ll_tups

def square_distance(x, y):
    return math.sqrt(sum([(xi - yi) ** 2 for xi, yi in zip(x, y)]))

def split_list_half(workorders):
    ll_tups = get_ll_tuples(valid_wo)
    tup_map = {}
    # get tuple map to get wo obj for lat lon tuple
    for idx, tup in enumerate(ll_tups):
        tup_map[tup] = valid_wo[idx]
    # get two furthest points
    max_square_distance = 0
    for pair in combinations(ll_tups, 2):
        if square_distance(*pair) > max_square_distance:
            max_square_distance = square_distance(*pair)
            max_pair = pair
    max_a = tup_map[max_pair[0]]
    max_a_tup = max_pair[0]
    ll_tups.remove(max_pair[0])
    max_b = tup_map[max_pair[1]]
    ll_tups.remove(max_pair[1])
    max_b_tup = max_pair[1]
    print("max_a: {}".format(max_a.pot_loc.format_addr))
    print("max_b: {}".format(max_b.pot_loc.format_addr))
    routeA = []
    routeB = []
    # keep getting nearest
    while ((len(routeA) < (MAX_WAYPOINTS - 1))
           and (len(routeB) < (MAX_WAYPOINTS - 1))
           and (len(ll_tups) >= 2)):
        min_a = get_nearest(max_a_tup, ll_tups)
        routeA.append(tup_map[min_a])
        ll_tups.remove(min_a)
        min_b = get_nearest(max_b_tup, ll_tups)
        routeB.append(tup_map[min_b])
        ll_tups.remove(min_b)
    routeA.insert(0, max_a)
    routeB.insert(0, max_b)
    return (routeA, routeB)

def get_nearest(origin, tups):
    min_square_distance = 999999999
    for tup in tups:
        if square_distance(origin, tup) < min_square_distance:
            min_square_distance = square_distance(origin, tup)
            min_tup = tup
    return min_tup

def get_test_url(depot, waypoints):
    url = 'https://www.google.com/maps/dir/{}/'.format(depot.pot_loc.format_addr.replace(' ','+'))
    for wp in waypoints:
        url = '{}/{}'.format(url,wp.pot_loc.format_addr.replace(' ','+'))
    url = '{}/{}'.format(url,depot.pot_loc.format_addr.replace(' ', '+'))
    print(url)

def get_optimized_route(route):
    origin = route.pop(0)
    print(origin.pot_loc.format_addr)
    dest = route.pop(len(route) - 1)
    print(dest.pot_loc.format_addr)
    waypoint_addrs = []
    for wp in route:
        waypoint_addrs.append(wp.pot_loc.format_addr)
    waypoint_str = '|'.join(waypoint_addrs)
    waypoint_str = '{}|{}'.format('optimize:true', waypoint_str)
    payload = {'origin': '{}'.format(origin.pot_loc.format_addr),
               'destination': '{}'.format(dest.pot_loc.format_addr),
               'waypoints': waypoint_str,
               'key': directions_api_key,
              }
    goog_data = requests.get(dir_url, params=payload)
    data = goog_data.json()
    order = data['routes'][0]['waypoint_order']
    for idx, val in enumerate(order):
        order[idx] = int(val)
    url = 'https://www.google.com/maps/dir/{}/'.format(origin.pot_loc.format_addr.replace(' ','+'))
    for idx in order:
        url = '{}/{}'.format(url,waypoint_addrs[idx].replace(' ','+'))
    url = '{}/{}'.format(url,dest.pot_loc.format_addr.replace(' ', '+'))
    return url

valid_wo = get_valid_workorders(sanity_wo)

(route1, route2) = split_list_half(valid_wo)
#get_test_url(depot, route1)
#get_test_url(depot, route2)
route1.insert(0, depot)
route1.insert(len(route1), depot)
route2.insert(0, depot)
route2.insert(len(route2), depot)
print(get_optimized_route(route1))
print(get_optimized_route(route2))

origin_wo = depot
dest_wo = depot

waypoints = []
for loc in valid_wo:
    waypoints.append(loc.pot_loc.format_addr)
waypoints = waypoints[0:22]

waypoint_str = "|".join(waypoints)
waypoint_str = '{}|{}'.format('optimize:true', waypoint_str)

payload = {'origin': '{}'.format(origin_wo.pot_loc.format_addr),
           'destination': '{}'.format(dest_wo.pot_loc.format_addr),
           'waypoints': waypoint_str,
           'key': directions_api_key,
          }
#print(payload)

goog_data = requests.get(dir_url, params=payload)
data = goog_data.json()

#print(data)
#print(data.keys())

order = data['routes'][0]['waypoint_order']
#print(order)
for idx, val in enumerate(order):
    order[idx] = int(val)

url = 'https://www.google.com/maps/dir/{}/'.format(origin_wo.pot_loc.format_addr.replace(' ','+'))
for idx in order:
    url = '{}/{}'.format(url,valid_wo[idx].pot_loc.format_addr.replace(' ','+'))
url = '{}/{}'.format(url,dest_wo.pot_loc.format_addr.replace(' ', '+'))

#print(url)
