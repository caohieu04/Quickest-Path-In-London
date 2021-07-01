# %%
from connection_handler import *
import gmplot
import json
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)


if __name__ == '__main__':
    apikey = 'AIzaSyDC4G5MMotPIKYgl6ow2AkNpfAkWwGKwCM'
    with open('../../Data/connection.json') as f:
        data = json.load(f)
    print("Data Loaded!")

# %%


def draw_line(paths, gmap, path_color):
    if isinstance(paths, list):
        ploted = False
        for path, color in zip(paths, path_color):
            gmap.plot(*path, edge_width=2, color=color)
            ploted = True
        # gmap.draw('map.html')
        # print(gmap.get()[:-1743])
        with open ("map-te.html", "r") as myfile:
            data = myfile.read()
        result = gmap.get()[:-1743] + data
        with open("map.html", "w") as f:
            f.write(result)
        # if ploted:
        #     print("Drawed")

BIAS_LAT = -7e-06
BIAS_LON = +4.5e-05

#path is zip(*[(,), (,)])
def draw_path(paths, data, lat, lon, zoom, name1, name2, src, des, path_color):
    paths = list(paths)
    apikey = 'AIzaSyDC4G5MMotPIKYgl6ow2AkNpfAkWwGKwCM'
    gmap = gmplot.GoogleMapPlotter(lat, lon, zoom, apikey=apikey)
    gmap.enable_marker_dropping('orange', draggable=True)
    if name1 == None:
        name1 = "First place"
    if name2 == None:
        name2 = "Second place"
    src = (src['lat'], src['lon'])
    des = (des['lat'], des['lon'])
    gmap.marker(src[0], src[1], color='white', title=name1)
    gmap.marker(des[0], des[1], color='black', title=name2)
    draw_line(paths, gmap, path_color)


if __name__ == '__main__':
    desired_idx = 300
    lat, lon = get_location(desired_idx, data)
    gmap = gmplot.GoogleMapPlotter(lat, lon, 15, apikey=apikey)
    depth = 100
    draw_line(get_random_way(desired_idx, data,
              depth, BIAS_LAT, BIAS_LON), gmap)
# import pickle
    # with open('map_plot', 'rb') as f:
    #     paths = pickle.load(f)
# %%
