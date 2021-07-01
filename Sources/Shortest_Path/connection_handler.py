import draw_map
# BIAS_LAT = draw_map.BIAS_LAT
# BIAS_LON = draw_map.BIAS_LON

# def load_data():
#   import json
#   with open('../../Data/connection.json') as f:
#     data = json.load(f)
#   return data
  
def get_out_edge(desired_idx, data):
  result = []
  for i, (k, v) in enumerate(data.items()):
    if i < desired_idx:
      continue
    if i > desired_idx:
      break
    if i == desired_idx:
      for out_node in v['connection']:
        lat = data[str(out_node['node_id'])]['lat'] 
        lon = data[str(out_node['node_id'])]['lon'] 
        lis = zip(*[
          (v['lat'], v['lon']),
          (lat, lon)
        ])
        result.append(lis)
  return result
def get_random_way(desired_idx, data, depth, BIAS_LAT, BIAS_LON):
  print("Current bias", BIAS_LAT, BIAS_LON)
  result = []
  for i, (k, v) in enumerate(data.items()):
    if i < desired_idx:
      continue
    if i > desired_idx:
      break
    if i == desired_idx:
      cur_node = v
      #trc_node: node which walked
      trc_node = set()
      trc_node.add(int(cur_node['node_id']))
      while depth > 0:
        #find next node
        nxt_node = None
        for node in cur_node['connection']:
          if int(node['node_id']) not in trc_node:
            trc_node.add(int(node['node_id']))
            nxt_node = data[str(node['node_id'])]
        if nxt_node == None:
          break
        
        lis = zip(*[
            (cur_node['lat'] + BIAS_LAT, cur_node['lon'] + BIAS_LON),
            (nxt_node['lat'] + BIAS_LAT, nxt_node['lon'] + BIAS_LON)
          ])
        result.append(lis)
        cur_node = nxt_node
        depth -= 1
  return result

def get_location(desired_idx, data):
  for i, (k, v) in enumerate(data.items()):
    if i < desired_idx:
      continue
    if i == desired_idx:
      return (v['lat'], v['lon'])
  
def to_map_plot(desired_idx, data, func):
  # import pickle
  plot_data = get_out_edge(data, desired_idx)
  # with open('map_plot', 'wb') as f:
  #   pickle.dump(plot_data, f)
  return plot_data
