# %%
import time
import json
import heapq
import os
import phase_4
from typing import Optional

from fastapi import FastAPI
from draw_map import *
import math
import numpy as np
from math import cos, asin, sqrt, pi
import matplotlib.pyplot as plt
from matplotlib import patches
import random
with open('../../Data/connection.json', encoding='utf-8') as f:
	data = json.load(f)
data_list = list(data.items())
d = {}
alroad = ['bridleway', 'steps', 'primary_link', 'service', 'unclassified', 'path', 'tertiary_link', 'pedestrian', 'raceway', 'trunk', 'no', 'motorway', 
           'motorway_link', 'rest_area', 'cycleway', 'secondary_link', 'trunk_link', 'road', 'secondary', 'living_street', 'corridor', 'track', 'construction', 
           'elevator', 'residential', 'tertiary', 'primary', 'proposed', 'footway']
lgroad = ['primary_link', 'trunk_link', 'primary', 'motorway', 'motorway_link', 'secondary_link', 'trunk', 'secondary', 'tertiary', 'tertiary_link']
meroad = ['corridor', 'raceway', 'elevator', 'unclassified', 'service', 'bridleway', 'footway']
groad = lgroad + ['residential', 'living_street', 'pedestrian', 'unclassified']
def sh(src="25508580", des="248996302", by="time"):
	d[src] = 0
	q = []
	trc = {}
	trc[src] = src

	heapq.heappush(q, (0, src))
	visited = []
	step = 0
	while len(q) > 0:
		step += 1
		k, u = heapq.heappop(q)
		visited.append(u)
		if k != d[u] or u not in data or 'connection' not in data[u]:
			continue
		for v_node in data[u]['connection']:
			if v_node['highway'] not in groad:
				continue
			v = str(v_node['node_id'])
			cost = v_node['distance'] if by=="dis" else v_node['time_travel']
			# bias = disab(v, des, "time")
			# print(bias, cost)
			# print(u, v)
			if v not in d:
				d[v] = 1e15
			if d[v] > d[u] + cost:
				# print(d[u], d[v], cost)
				d[v] = d[u] + cost
				trc[v] = u
				heapq.heappush(q, (d[v], str(v)))
		# if step % 1000 == 0:
		# 	q = sorted(q, key = lambda x: disab(x[1], des))
	return None
#%%
sh()
new_data = {}
for k, v in data_list:
  if k in d:
    new_data[k] = v
with open('new_highways.json', 'w', encoding='utf-8') as f:
  json.dump(new_data, f, ensure_ascii=False, indent=2)