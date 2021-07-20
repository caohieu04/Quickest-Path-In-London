 
import time
import json
import heapq
import os
from Trie.trie import Trie
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

app = FastAPI()
def groad_get():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  os.chdir(dir_path)
  alroad = ['bridleway', 'steps', 'primary_link', 'service', 'unclassified', 'path', 'tertiary_link', 'pedestrian', 'raceway', 'trunk', 'no', 'motorway', 
           'motorway_link', 'rest_area', 'cycleway', 'secondary_link', 'trunk_link', 'road', 'secondary', 'living_street', 'corridor', 'track', 'construction', 
           'elevator', 'residential', 'tertiary', 'primary', 'proposed', 'footway']
  lgroad = ['primary_link', 'trunk_link', 'primary', 'motorway', 'motorway_link', 'secondary_link', 'trunk', 'secondary', 'tertiary', 'tertiary_link']
  meroad = ['corridor', 'raceway', 'elevator', 'unclassified', 'service', 'bridleway', 'footway']
  groad = ['motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link', 'residential', 'living_street', 'pedestrian', 'unclassified']
  return groad

def color_map_get():
  # color = ['crimson', 'crimson', 'coral', 'coral', 'gold', 'gold', 'limegreen', 'limegreen', 'cyan', 'cyan', 'deepskyblue', 'mediumblue', 'blueviolet', 'fuchsia']
  color = ['crimson', 'crimson', 'coral', 'coral', 'yellow', 'yellow', 'limegreen', 'limegreen', 'aqua', 'aqua', 'deepskyblue', 'mediumblue', 'blueviolet', 'fuchsia']
  # color = color[::-1]
  road_color = dict(zip(groad, color))
   
  color_map = {}
  for u, v in data_list:
    for k in v.get('connection', []):
      if k['highway'] in groad:
        color_map[(str(v['node_id']), str(k['node_id']))] = road_color[k['highway']]
        color_map[(str(k['node_id']), str(v['node_id']))] = road_color[k['highway']]
  return color_map
 
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
def find_shortest_path(src="3533830193", des="4866976610", by="time"):
  d = {}
  d[src] = 0
  q = []
  trc = {}
  trc[src] = src
  # print(src, des)
  heapq.heappush(q, (0, src))
  visited = []
  step = 0
  while len(q) > 0:
    step += 1
    k, u = heapq.heappop(q)
    visited.append(u)
    if u == des:
      nodes = []
      while trc[u] != u:
        nodes.append(u)
        u = trc[u]
      nodes.append(u)
      desired_idx = nodes[len(nodes) // 2]
      paths = []
      paths_color = []
      for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]
        lis = zip(*[
          (data[u]['lat'] + BIAS_LAT, data[u]['lon'] + BIAS_LON),
          (data[v]['lat'] + BIAS_LAT, data[v]['lon'] + BIAS_LON)
        ])
        paths.append(lis)
        paths_color.append(color_map[(u, v)])
      lat = data[nodes[len(nodes) // 2]]['lat']
      lon = data[nodes[len(nodes) // 2]]['lon']
      dis = disab(src, des)
      zoom = math.log2(64000 / dis)
      name1 = data[src].get('name', None)
      name2 = data[des].get('name', None)
      draw_path(paths, data, lat, lon, zoom, name1, name2, data[src], data[des], paths_color)
      return k, step
    if k != d[u] or u not in data or 'connection' not in data[u]:
      continue
    for v_node in data[u]['connection']:
      if v_node['highway'] not in groad:
        continue
      v = str(v_node['node_id'])
      cost = v_node['distance'] if by=="dis" else v_node['time_travel']
      if v not in d:
        d[v] = 1e15
      if d[v] > d[u] + cost:
         
        d[v] = d[u] + cost
        trc[v] = u
        heapq.heappush(q, (d[v], str(v)))
  return None
def find_all_paths(src="3533830193", des="4866976610", by="time", lim_step=10000):
  t1 = time.time()
  d = {}
  d[src] = 0
  q = []
  trc = {}
  trc[src] = src

  heapq.heappush(q, (0, src))
  visited = []
  li_paths = []
  li_paths_color = []
  step = 0
  while len(q) > 0 and step <= lim_step:
    step += 1
    k, u = heapq.heappop(q)
    # print(k, u)
    visited.append(u)
    is_new_node = True
    if is_new_node:
      nodes = []
      while trc[u] != u:
        nodes.append(u)
        u = trc[u]
        break
      nodes.append(u)
      paths = []
      paths_color = []
      for i in range(len(nodes) - 1):
        u = nodes[i]
        v = nodes[i + 1]
        lis = zip(*[
          (data[u]['lat'], data[u]['lon']),
          (data[v]['lat'], data[v]['lon'])
        ])
        paths.append(lis)
        paths_color.append(color_map[(u, v)])
      li_paths.append(paths)
      li_paths_color.append(paths_color)
    if k != d[u] or u not in data or 'connection' not in data[u]:
      continue
    for v_node in data[u]['connection']:
      if v_node['highway'] not in groad:
        continue
      v = str(v_node['node_id'])
      cost = v_node['distance'] if by=="dis" else v_node['time_travel']
      if v not in d:
        d[v] = 1e15
      if d[v] > d[u] + cost:
        d[v] = d[u] + cost
        trc[v] = u
        heapq.heappush(q, (d[v], str(v)))
  draw_li_path(li_paths, data, DEFAULT_LAT, DEFAULT_LON, 13, li_paths_color)
  return time.time() - t1
  
def build_trie():
  global li_named_node
  name2id = {}
  for _, u in data_list:
    if "name" in u:
      li_named_node.append(u["name"].lower())
      name2id[u["name"].lower()] = u['node_id']
    if "connection" in u:
      for v in u["connection"]:
        if "name" in v:
          li_named_node.append(v["name"].lower())
          name2id[v["name"].lower()] = u['node_id']
  li_named_node = list(set(li_named_node))
  print(f"Number of named node: {len(li_named_node)}")
  
  """
  1. Create Trie
  2. Add data to Trie
  """
  trie = Trie()
  trie.add_all(li_named_node)

  return trie, name2id


def nearest_name_get(search):
  result_str = None
  search = search.lower()
  if search == '':
    result_str = trie.search_with_wildcard('*')
  else:
    result_str = trie.search_with_wildcard('*' +
                        '*'.join([*search[::1]]) +
                        '*')
  if len(result_str) == 0:
    result_str = [li_named_node[random.randint(0, len(li_named_node))]]
  result = (name2id.get(result_str[0]), result_str[0])
  return result

def build_quadtree(k=100, data_list=None, b_draw_map=False):
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
    def __init__(self, k, data_list):
      self.threshold = k
      self.points = []
      for _, u in data_list:
        self.points.append(Point(u['lat'], u['lon']))	 
      self.root = Node(DEFAULT_LAT, DEFAULT_LON, 0.5, 1, self.points)

    def add_point(self, x, y):
      self.points.append(Point(x, y))
    
    def get_points(self):
      return self.points
    
    def subdivide(self):
      recursive_subdivide(self.root, self.threshold)
    
    def graph(self):
      fig = plt.figure(figsize=(120, 120))
      plt.title("Quadtree")
      ax = fig.add_subplot(111)
      c = find_children(self.root)
      print("Number of segments: %d" %len(c))
      areas = set()
      for el in c:
        areas.add(el.width*el.height)
      for n in c:
        ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False, lw=0.5))
      x = [point.x for point in self.points]
      y = [point.y for point in self.points]
      plt.plot(x, y, 'Hr', markersize=0.7, fillstyle='full')
      print("Minimum segment area: %.10f units" %min(areas))
      plt.savefig('quadtree.png', format='png', dpi=300)
      print("Quadtree visualized!")
      # plt.show()
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

  # lats = []
  # lons = []
  # for u in data_list:
  # 	lats.append(u[1]['lat'])
  # 	lons.append(u[1]['lon'])
  q_tree = QTree(k, data_list)
  q_tree.subdivide()
  if b_draw_map:
    q_tree.graph() 

class KdTree:
  def __init__(self, data) -> None:
    points = []
    for _, u in data_list:
      points.append((u['lat'], u['lon']))
      pos2id[(int(u['lat'] * 100000000), int(u['lon'] * 100000000))] = u['node_id']
    self.KDTree = self.make_kd_tree(points)

  def dist_square(self, a, b):
    return distance(a[0], a[1], b[0], b[1])
     

  def make_kd_tree(self, points):
    def make_kd_tree_fn(point, i=0):
      if len(point) > 1:
        point.sort(key=lambda x: x[i])
         
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

   
  def add_point(self, point_add):
    def add_point_fn(kd_tree, point, i=0):
       
      dx = kd_tree[2][i] >= point[i]
       
      j = (0 if dx else 1)
       
      i = (i + 1) % 2

      if kd_tree[j] is None:
        kd_tree[j] = [None, None, point]
      else:
        add_point_fn(kd_tree[j], point, i)

    return add_point_fn(self.KDTree, point_add)

   
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
         
        for b in [dx < 0] + [dx >= 0] * (dx * dx < -heap[0][0]):
          get_knn_fn(kd_tree[b], point, k, i, heap)
      if is_root:
        neighbors = sorted([-h[0], h[1]] for h in heap)
        return neighbors

    return get_knn_fn(self.KDTree, search, k, 0, None)

   
  def get_nearest(self, search):
    def get_nearest_fn(kd_tree, point, i=0, best=None):
      if kd_tree is not None:
         
        dist = self.dist_square(point, kd_tree[2])
        dx = kd_tree[2][i] - point[i]
         
        if not best:
          best = [dist, kd_tree[2]]
        elif dist < best[0]:
          best[0], best[1] = dist, kd_tree[2]
        
         
        i = (i + 1) % 2
         
        for b in [dx < 0] + [dx >= 0] * (dx * dx < best[0]):
          get_nearest_fn(kd_tree[b], point, i, best)
      return best

    return get_nearest_fn(self.KDTree, search, 0, None)
 
def get_pos_to_id(point):
  pin = KD.get_nearest(point)[1]
  return pos2id[(int(pin[0] * 100000000), int(pin[1] * 100000000))]
@app.get("/byPos/")
def find_by_pos(p1lat: float, p1lon: float, p2lat: float, p2lon: float):
  print("=" * 30 + "find_by_pos" + "=" * 30)
  t1 = time.time()
  point1 = (p1lat, p1lon)
  point2 = (p2lat, p2lon)
  point1 = str(get_pos_to_id(point1))
  point2 = str(get_pos_to_id(point2))
  t2 = time.time() - t1
  print(f"Runtime for get_pos_to_id: {t2}")
  t1 = time.time()
  re, step = find_shortest_path(point1, point2)
  t2 = time.time() - t1
  print(f"Runtime for sh: {t2}")
  print(f"  Num steps: {step}")
  print(f"Output: {re}")
  return re, t2

@app.get("/byName/")
def find_by_name(name1, name2):
  print("=" * 30 + "find_by_name" + "=" * 30)
  t1 = time.time()
  a = nearest_name_get(name1)
  b = nearest_name_get(name2)
  t2 = time.time() - t1
  print(f"find_by_name: {a} and {b} with {t2:.4f}")
  t1 = time.time()
  re, step = find_shortest_path(str(a[0]), str(b[0]))
  t2 = time.time() - t1
  print(f"Runtime for sh: {t2}")
  print(f"  Num steps: {step}")
  return re, t2
@app.get("/paths")
def print_map(lim_step: int=10000):
  print("=" * 30 + "print_map" + "=" * 30)
  print(f"lim_step: {lim_step}")
  ti = find_all_paths(lim_step=lim_step)
  return ti
 
# if __name__ == "__main__":
DEFAULT_LAT=51.5074329
DEFAULT_LON=-0.1283836
BIAS_LAT=-7e-06
BIAS_LON=+4.5e-05
      
print("Starting..")
start_up_t1 = time.time()
with open('../../Data/connection.json', encoding='utf-8') as f:
  data = json.load(f)
data_list = list(data.items())
groad = groad_get()
color_map = color_map_get()
print(f'Number of nodes: {len(data_list)}')
find_all_paths(lim_step=30000)
print(f'Read time: {time.time() - start_up_t1}')

t = time.time()
li_named_node = []
trie, name2id = build_trie()
pos2id = {}
print(f"Runtime for Trie {time.time() - t}")

t = time.time()
KD = KdTree(data_list)
print(f"Runtime for KDTree {time.time() - t}")

# t = time.time()
# build_quadtree(k=100, data_list=data_list, b_draw_map=False)
# print(f"Runtime for QTree {time.time() - t}")

start_up_t2 = time.time() - start_up_t1
print(f"Start up time: {start_up_t2}")