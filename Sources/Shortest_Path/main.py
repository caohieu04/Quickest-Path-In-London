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
start_up_t1 = time.time()
with open('../../Data/connection.json', encoding='utf-8') as f:
	data = json.load(f)
data_list = list(data.items())
print(f'Read time: {time.time() - start_up_t1}')
app = FastAPI()
def groad_get():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(dir_path)
	# print(len(data))
	# print(data_list[100000])
	# print(data_list[200000])
	# se = []
	# for u, v in data_list:
	# 	for k in v.get('connection', []):
	# 		se.append(k.get('highway', 'null'))
	# se = set(se)
	alroad = ['bridleway', 'steps', 'primary_link', 'service', 'unclassified', 'path', 'tertiary_link', 'pedestrian', 'raceway', 'trunk', 'no', 'motorway', 
					 'motorway_link', 'rest_area', 'cycleway', 'secondary_link', 'trunk_link', 'road', 'secondary', 'living_street', 'corridor', 'track', 'construction', 
					 'elevator', 'residential', 'tertiary', 'primary', 'proposed', 'footway']
	lgroad = ['primary_link', 'trunk_link', 'primary', 'motorway', 'motorway_link', 'secondary_link', 'trunk', 'secondary', 'tertiary', 'tertiary_link']
	meroad = ['corridor', 'raceway', 'elevator', 'unclassified', 'service', 'bridleway', 'footway']
	groad = ['motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'living_street', 'pedestrian', 'unclassified']
	return groad
groad = groad_get()
print(f'Number of node: {len(data_list)}')
def color_map_get():
	color = ['crimson', 'crimson', 'coral', 'coral', 'gold', 'gold', 'limegreen', 'limegreen', 'cyan', 'cyan', 'deepskyblue', 'mediumblue', 'blueviolet', 'fuchsia']
	road_color = dict(zip(groad, color))
	# print(road_color)
	color_map = {}
	for u, v in data_list:
		for k in v.get('connection', []):
			if k['highway'] in groad:
				color_map[(str(v['node_id']), str(k['node_id']))] = road_color[k['highway']]
				color_map[(str(k['node_id']), str(v['node_id']))] = road_color[k['highway']]
	return color_map
color_map = color_map_get()
# %%

def distance(lat1, lon1, lat2, lon2):
	p = pi/180
	a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
	return 7917.5117 * asin(sqrt(a)) 
def disab(a, b, by='distance'):
	a = str(a)
	b = str(b)
	alat = data[a]['lat']
	alon = data[a]['lon']
	blat = data[b]['lat']
	blon = data[b]['lon']
	re = distance(alat, alon, blat, blon)
	if by=="time":
		re /= 40
	return re
def sh(src="35964104", des="248996302", by="time"):
	d = {}
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
		if u == des:
			BIAS_LAT = -7e-06
			BIAS_LON = +4.5e-05
			path = []
			while trc[u] != u:
				path.append(u)
				u = trc[u]
			path.append(u)
			desired_idx = path[len(path) // 2]
			print(f"Number of node in path: {len(path)}")
			
			path_split = []
			path_color = []
			for i in range(len(path) - 1):
				u = path[i]
				v = path[i + 1]
				lis = zip(*[
					(data[u]['lat'] + BIAS_LAT, data[u]['lon'] + BIAS_LON),
					(data[v]['lat'] + BIAS_LAT, data[v]['lon'] + BIAS_LON)
				])
				path_split.append(lis)
				path_color.append(color_map[(u, v)])
			lat = data[path[len(path) // 2]]['lat']
			lon = data[path[len(path) // 2]]['lon']
			dis = disab(src, des)
			zoom = math.log2(64000 / dis)
			name1 = data[src].get('name', None)
			name2 = data[des].get('name', None)
			draw_path(path_split, data, lat, lon, zoom, name1, name2, data[src], data[des], path_color)
			return k
			break
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
			
			


# t = time.time()
# print(sh())
# print(time.time() - t)

# mi = 1e18
# pin = (data_list[200000][1]['lat'], data_list[200000][1]['lon'])
# for point in data_list:
#     k = distance(point[1]['lat'], point[1]['lon'], pin[0], pin[1])
#     if k < mi:
#         mi = k

# # print(disab(100000, 200000))
# print(time.time() - t)


# %%
def build_edit_distance():
	
	name2id = {}
	matrix = []
	for i in range(100):
		new = []
		for j in range(100):
			new.append(0)
		matrix.append(new)
	class editDistance:
		#stringData: data_list
		def __init__(self, stringData):
			re = []
			for _, u in stringData:
				# print(u[1])
				# break
				if "name" in u:
					re.append(u["name"].lower())
					name2id[u["name"].lower()] = u['node_id']
				if "connection" in u:
					for v in u["connection"]:
						if "name" in v:
							re.append(v["name"].lower())
							name2id[v["name"].lower()] = u['node_id']
			re = set(re)
			print(f"Number of named node: {len(re)}")
			self.stringData = re
			
		def compute_edit_dist(self, string1, string2):
			# + 1 for 1 more row to contain order of character in string
			m = len(string1) + 1
			n = len(string2) + 1
			for i in range(m):
				for j in range(n):
					matrix[i][j] = 0

			for i in range(m):
				matrix[i][0] = i
			for j in range(n):
				matrix[0][j] = j

			for i in range(1, m):
				for j in range(1, n):
					if string1[i-1] == string2[j-1]:
						matrix[i][j] = matrix[i-1][j-1]
					else:
						# Replace][ insertion][ deletion
						matrix[i][j] = 1 + min(matrix[i-1][j-1], matrix[i-1][ j], matrix[i][ j-1])
			dist = matrix[m-1][n-1]
			return dist
		
		def nearest_name_get(self, search, top_n=1):
			dist_scores = []
			mi = 1e15
			for v in self.stringData:
				dist = self.compute_edit_dist(search, v)
				if int(dist) < mi:
					mi = dist
					re = (name2id[v], v)
				# dist_scores.append((k, v, int(dist)))
			# print(dist_scores)
			# dist_scores = sorted(dist_scores, key=lambda x: x[2],reverse=False)
			return re
	return editDistance(data_list)

ED = build_edit_distance()

# %%
# t = time.time()
# name1 = "lo hill"
# name2 = "buck"
@app.get("/byName/")
def findByName(name1, name2):
	t1 = time.time()
	a = ED.nearest_name_get(name1)
	b = ED.nearest_name_get(name2)
	re = sh(str(a[0]), str(b[0]))
	t2 = time.time() - t1
	return re, t2
# findByName(name1, name2)
# print(ED.nearest_name_get("summy side"))
# print(time.time() - t)
# print(data_list[1])
# %%
# print(data[str(7942016572)])
# %%
def build_quadtree():

	class Point():
		def __init__(self, x, y):
			self.x = x
			self.y = y

	class Node():
		def __init__(self, x0, y0, w, h, points):
			self.x0 = x0
			self.y0 = y0
			self.width = w
			self.height = h
			self.points = points
			self.children = []

		def get_width(self):
			return self.width

		def get_height(self):
			return self.height

		def get_points(self):
			return self.points

	class QTree():
		def __init__(self, k, n, data_list):
			self.threshold = k
			self.points = []
			for _, u in data_list:
				self.points.append(Point(u['lat'], u['lon']))
			# self.points = [Point(random.uniform(0, 10), random.uniform(0, 10)) for x in range(n)]
			self.root = Node(51.2822035, -0.5177851, 0.5, 1, self.points)

		def add_point(self, x, y):
			self.points.append(Point(x, y))
		
		def get_points(self):
			return self.points
		
		def subdivide(self):
			recursive_subdivide(self.root, self.threshold)
		
		def graph(self):
			fig = plt.figure(figsize=(60, 60))
			plt.title("Quadtree")
			ax = fig.add_subplot(111)
			c = find_children(self.root)
			print("Number of segments: %d" %len(c))
			areas = set()
			for el in c:
				areas.add(el.width*el.height)
			print("Minimum segment area: %.3f units" %min(areas))
			for n in c:
				ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
			x = [point.x for point in self.points]
			y = [point.y for point in self.points]
			plt.plot(x, y, 'ro', markersize=0.1)
			print("Quadtree showed")
			plt.savefig('quadtree.png')
			plt.show()
			return

	def recursive_subdivide(node, k):
		if len(node.points)<=k:
			return
		
		w_ = float(node.width/2)
		h_ = float(node.height/2)

		p = contains(node.x0, node.y0, w_, h_, node.points)
		x1 = Node(node.x0, node.y0, w_, h_, p)
		recursive_subdivide(x1, k)

		p = contains(node.x0, node.y0+h_, w_, h_, node.points)
		x2 = Node(node.x0, node.y0+h_, w_, h_, p)
		recursive_subdivide(x2, k)

		p = contains(node.x0+w_, node.y0, w_, h_, node.points)
		x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
		recursive_subdivide(x3, k)

		p = contains(node.x0+w_, node.y0+h_, w_, h_, node.points)
		x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p)
		recursive_subdivide(x4, k)

		node.children = [x1, x2, x3, x4]
		
		
	def contains(x, y, w, h, points):
		pts = []
		for point in points:
			if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
				pts.append(point)
		return pts


	def find_children(node):
		if not node.children:
			return [node]
		else:
			children = []
			for child in node.children:
				children += (find_children(child))
		return children

	lats = []
	lons = []
	for u in data_list:
		lats.append(u[1]['lat'])
		lons.append(u[1]['lon'])
	# print(min(lats), max(lats))
	# print(min(lons), max(lons))
	# print(len(Q.points))
	Q = QTree(10, 3, data_list=data_list[:100000])
	t = time.time()
	Q.subdivide()
	Q.graph()
	print(f"Runtime for Quadtree: {time.time() - t}")
# build_quadtree()
# %%
pos2id = {}
class KdTree:
	def __init__(self, data) -> None:
		points = []
		for _, u in data_list:
			points.append((u['lat'], u['lon']))
			pos2id[(int(u['lat'] * 100000000), int(u['lon'] * 100000000))] = u['node_id']
		self.KDTree = self.make_kd_tree(points)

	def dist_square(self, a, b):
		return distance(a[0], a[1], b[0], b[1])
		# return (b[0] - a[0])**2 + (b[1] - a[1])**2

	def make_kd_tree(self, points):
		def make_kd_tree_fn(point, i=0):
			if len(point) > 1:
				point.sort(key=lambda x: x[i])
				# i dùng để so sánh
				i = (i + 1) % 2
				half = len(point) >> 1
				return [
					make_kd_tree_fn(point[: half], i),
					make_kd_tree_fn(point[half + 1:], i),
					point[half]
				]
			elif len(point) == 1:
				return [None, None, point[0]]
		return make_kd_tree_fn(points)

	# Adds a point to the kd-tree
	def add_point(self, point_add):
		def add_point_fn(kd_tree, point, i=0):
			# dx dùng để lấy j
			dx = kd_tree[2][i] >= point[i]
			# j để vô node trái or phải
			j = (0 if dx else 1)
			# i là dim dùng để so sánh
			i = (i + 1) % 2

			if kd_tree[j] is None:
				kd_tree[j] = [None, None, point]
			else:
				add_point_fn(kd_tree[j], point, i)

		return add_point_fn(self.KDTree, point_add)

	# k nearest neighbors
	def get_knn(self, search, k=5):
		def get_knn_fn(kd_tree, point, k, i=0, heap=None):
			is_root = not heap
			if is_root:
				heap = []
			if kd_tree is not None:
				dist = self.dist_square(point, kd_tree[2])
				dx = kd_tree[2][i] - point[i]

				if len(heap) < k:
					heapq.heappush(heap, (-dist, kd_tree[2]))
				elif dist < -heap[0][0]:
					heapq.heappushpop(heap, (-dist, kd_tree[2]))
				i = (i + 1) % 2
				# Goes into the left branch, and then the right branch if needed
				for b in [dx < 0] + [dx >= 0] * (dx * dx < -heap[0][0]):
					get_knn_fn(kd_tree[b], point, k, i, heap)
			if is_root:
				neighbors = sorted([-h[0], h[1]] for h in heap)
				return neighbors

		return get_knn_fn(self.KDTree, search, k, 0, None)

	# For the closest neighbor
	def get_nearest(self, search):
		def get_nearest_fn(kd_tree, point, i=0, best=None):
			if kd_tree is not None:
				# Tính khoảng cách giữa 2 điểm
				dist = self.dist_square(point, kd_tree[2])
				dx = kd_tree[2][i] - point[i]
				# Nếu chưa có best
				if not best:
					best = [dist, kd_tree[2]]
				elif dist < best[0]:
					best[0], best[1] = dist, kd_tree[2]
				
				# i là dim để so sánh
				i = (i + 1) % 2
				# Goes into the left branch, and then the right branch if needed
				for b in [dx < 0] + [dx >= 0] * (dx * dx < best[0]):
					get_nearest_fn(kd_tree[b], point, i, best)
			return best

		return get_nearest_fn(self.KDTree, search, 0, None)

t = time.time()
KD = KdTree(data_list)
print(f"Runtime for KDTree {time.time() - t}")
# %%
def getPosToId(point):
	pin = KD.get_nearest(point)[1]
	return pos2id[(int(pin[0] * 100000000), int(pin[1] * 100000000))]
@app.get("/byPos/")
def findByPos(p1lat: float, p1lon: float, p2lat: float, p2lon: float):
	t1 = time.time()
	point1 = (p1lat, p1lon)
	point2 = (p2lat, p2lon)
	point1 = str(getPosToId(point1))
	point2 = str(getPosToId(point2))
	t2 = time.time() - t1
	# print(data[point1])
	# print(data[point2])
	print("=" * 30 + "findByPos" + "=" * 30)
	re = sh(point1, point2)
	print(f"Runtime for getPosToId: {t2}")
	t2 = time.time() - t1
	print(f"Runtime for sh: {t2}")
	print(f"Output: {re}")
	return re, t2
start_up_t2 = time.time() - start_up_t1
print(f"Start up time: {start_up_t2}")
# re = findByPos(51.5, 0, 51.3, 0.2)
# print(re)
# %%
