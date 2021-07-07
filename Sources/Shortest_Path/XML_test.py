#%%
import xmltodict
import pprint
import json
import os
import math
ROOT_DIR = r'D:\GitHub\Learning'
os.chdir(ROOT_DIR)

with open('./Data/highways.osm', encoding='utf-8') as fd:
    doc = xmltodict.parse(fd.read())

# %%
print(len(doc['osm']['node']))
def node(te):
  re = {}
  re['node_id'] = int(te['@id'])
  re['lat'] = float(te['@lat'])
  re['lon'] = float(te['@lon'])
  if 'tag' in te:
    if isinstance(te['tag'], list):
      for t in te['tag']:
        # print(t)
        if t['@k'] == 'name':
          re['name_node'] = t['@v']
          break
    else:
      if te['tag']['@k'] == 'name':
        re['name_node'] = te['tag']['@v']
  return re
  
node_dic = {}
for i in range(len(doc['osm']['node'])):
  te  = doc['osm']['node'][i]
  te = node(te)
  node_dic[int(te['node_id'])] = te
  # pprint.pprint(dict(te.items()))
# %%
highways = {}
avg_highways_maxspeed = {'primary': 26.30113547198569, 'residential': 21.444809322033898, 'trunk': 34.143945050022396, 'trunk_link': 37.84455958549223, 'unclassified': 21.652526512788523, 'tertiary': 24.104497710746028, 'secondary': 23.3739837398374, 'motorway_link': 57.63819095477387, 'motorway': 64.30434782608695, 'primary_link': 29.364406779661017, 'cycleway': 19.486196319018404, 'service': 17.309849362688297, 'living_street': 20.535135135135135, 'pedestrian': 18.944162436548222, 'tertiary_link': 29.0990990990991, 'path': 18.363636363636363, 'secondary_link': 25.27777777777778, 'proposed': 20.0, 'footway': 20.147058823529413, 'construction': 22.307692307692307, 'track': 14.285714285714286, 'corridor': 30.0, 'steps': 22.0}
from math import cos, asin, sqrt, pi
def distance(lat1, lon1, lat2, lon2):
  p = pi/180
  a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
  return 7917.5117 * asin(sqrt(a)) #2*R*asin...
def time_travel(dis, maxi):
  return 1.0 * dis / maxi
print(len(doc['osm']['way']))

for id in range(len(doc['osm']['way'])):
  te  = doc['osm']['way'][id]
  connection = {}
  for S in ['name', 'highway', 'maxspeed', 'oneway']:
    loop_list = te['tag']
    if not isinstance(te['tag'], list):
      loop_list = [te['tag']]
    for t in loop_list:
      if t['@k'] == S:
        connection[S] = t['@v']
  
  if 'maxspeed' in connection:
    if connection['maxspeed'] == 'walk':
      connection['maxspeed'] = 3
    elif connection['maxspeed'] == 'signals':
      connection['maxspeed'] = 40
    else:
      connection['maxspeed'] = float(connection['maxspeed'].split()[0])
  else:
    if connection['highway'] in avg_highways_maxspeed:
      connection['maxspeed'] = avg_highways_maxspeed[connection['highway']]
    else:
      connection['maxspeed'] = 3
  if 'oneway' in connection:
      connection['oneway'] = True if connection['oneway'] == 'yes' else False
  #connection:dict of 1 way
          
  lis = []
  for t in te['nd']:
    lis.append(int(t['@ref']))
  #lis: list of node in way
  for i in range(len(lis) - 1):
    a = node_dic[lis[i]]
    b = node_dic[lis[i + 1]]
    if (a == b):
      continue
    #a, b: near node in a way
    new_node = connection.copy()
    new_node['distance'] = distance(a['lat'], a['lon'], b['lat'], b['lon'])
    new_node['time_travel'] = time_travel(new_node['distance'], new_node['maxspeed'])
    
    
    def add_edge(a, b, new_node):  
      new_node['node_id'] = b['node_id']
      if 'connection' not in a:
        a['connection'] = []
      non_asame = True
      for x in a['connection']:
        if x['node_id'] == new_node['node_id']:
          non_asame = False
      if a['node_id'] == b['node_id']:
        print(a['lat'], a['lon'], b['lat'], b['lon'])
        print(distance(a['lat'], a['lon'], b['lat'], b['lon']))
      if non_asame:
        a['connection'].append(new_node)
        
    if 'oneway' not in new_node or new_node['oneway'] == False:
      new_node_rev = new_node.copy()
      add_edge(b, a, new_node_rev)
    add_edge(a, b, new_node)

  # if (got == False):
  #   print("*")
  #   pprint.pprint(dict(te.items()))
#%%
# highways = 
{'elevator', 'motorway', 'tertiary_link', 'primary', 'secondary_link', 'trunk', 'services', 'construction', 'road', 
 'corridor', 'residential', 'steps', 'secondary', 'no', 'motorway_link', 'track', 'primary_link', 'living_street', 
 'raceway', 'unclassified', 'proposed', 'path', 'bridleway', 'rest_area', 'trunk_link', 'service', 'tertiary', 
 'pedestrian', 'footway', 'cycleway'}
#%%
for k, v in list(node_dic.items())[:100]:
  pprint.pprint(v)
  print("*")

# %%
with open('connection.json', 'w', encoding='utf8') as f:
  json.dump(node_dic, f, ensure_ascii=False, indent=2)
# %%
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
# %%
