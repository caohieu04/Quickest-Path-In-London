# Quickest path in London

## About
Extracting infomations of road networking in London from [openstreetmap](https://www.openstreetmap.org/), this can then run Dijsktra Algorithm to find shortest path. Using OpenAPI to implement server and Google Map API to get nice background map from Google. Slight tweak with heuristic approach: assuming one's velocity is road's max-speed, quickest route is obtained.

## Run Command
```
cd ./Sources/Shortest_Path
uvicorn main:app --reload
```

## Road Color

| Road                       | Color | |
|----------------------------|:----------------:|--------:|
| `motorway`                 | `crimson      `|![#DC143C](https://via.placeholder.com/15/DC143C/000000?text=+) |
| `trunk`                    | `coral        `|![#FF7F50](https://via.placeholder.com/15/FF7F50/000000?text=+)             | 
| `primary`                  | `yellow         `|![#FFFF00](https://via.placeholder.com/15/FFFF00/000000?text=+)           | 
| `secondary`                | `limegreen    `|![#32CD32](https://via.placeholder.com/15/32CD32/000000?text=+)   |
| `tertiary`                 | `aqua         `|![#00FFFF](https://via.placeholder.com/15/00FFFF/000000?text=+) | 
| `residential`              | `deepskyblue  `|![#00BFFF](https://via.placeholder.com/15/00BFFF/000000?text=+)           | 
| `living_street`            | `mediumblue   `|![#0000CD](https://via.placeholder.com/15/0000CD/000000?text=+)           | 
| `pedestrian`               | `blueviolet   `|![#8A2BE2](https://via.placeholder.com/15/8A2BE2/000000?text=+)     | 
| `unclassified`             | `fuchsia      `|![#FF00FF](https://via.placeholder.com/15/FF00FF/000000?text=+)    | 

## Demo Video

![](demo_.gif)

## Map Overview

![](Sources/Shortest_Path/map.png)


* Features:
    * Find by Name: Input 2 name, use Trie to search for node with nearest name, calculate the shortest path
    * Find by Location: Click by mouse on interactive map, use KD-Tree to search for node with nearest name, calculate the shortest path
## Performance:
* Start-up Time:
    * Read `connection.json`: ~8s 
    * KdTree: ~4s
    * Trie: ~1s
    * Qtree: ~60s (Use only once to produce `quadtree.png`)
    * Other: ~1s
    * Total: ~14s (non Qtree) && ~75s (Qtree)
* API Time:
    * Find By Name: ~1s (get places from name) + ~1s (quickest path)
    * Find By Location: ~1s (get nearest valid location from marker) + ~1s (quickest path)

## Quad Tree
![](Sources/Shortest_Path/qt3.png)

![](Sources/Shortest_Path/qt4.png)



## Technical
* Stats:
    * Nodes: ~560k
    * Named node: ~40k
    * `connection.json`: ~350mb
* Shortest Path:
  * Function sh(src, des, by):
      * `src` : source (node_id)(str)
      * `des` : destination (node_id)(str)
      * `by` : `time` or `distance` (str)
  * Class QTree:
      * `__init__(k, data_list)`:
          * `k`: threshold for number of point in smallest cell
          * `data_list`: `list(data.items())`
      * `add_point(point)`
      * `recursive_subdivide(node, k)`
      * `contains(x, y, w, h, points)`: Check if reactangle top left corner `(x, y)` size `(w, h)` contains all points
      * `find_children(node)`
      * `graph()`: Draw plt grap to `quadtree.png`
  * Class Trie:
      * `nearest_name_get(search)`: get nearest name compare to `search`
  * Class KdTree:
      * `__init__(data)`: 
          * `data`: from `connection.json`
      * `make_kd_tree(points)`: 
          * `points`: list of all points
      * `add_point(point)`
      * `get_nearest(point)`
 
 ## Team members: 
  * Cao Ngoc Hieu
  * Nguyen Gia Huy
  * Nguyen Tai Loc
