import numpy as np
import heapq

class editDistance:
    def __init__(self, stringData):
        self.stringData = stringData
        
    def _computeDist(self, string1, string2):
        # + 1 for 1 more row to contain order of character in string
        m = len(string1) + 1
        n = len(string2) + 1
        matrix = np.zeros((m, n))

        for i in range(m):
            matrix[i,0] = i
        for j in range(n):
            matrix[0,j] = j

        for i in range(1,m):
            for j in range(1,n):
                if string1[i-1] == string2[j-1]:
                    matrix[i,j] = matrix[i-1,j-1]
                else:
                    # Replace, insertion, deletion
                    matrix[i,j] = 1 + min(matrix[i-1,j-1], matrix[i-1, j], matrix[i, j-1])
        dist = matrix[m-1,n-1]
        return dist
    
    def nearestName(self, search,top_n=10):
        dist_scores = []
        for (k,v) in self.stringData:
            dist = self._computeDist(search.lower(), v.lower())
            
            dist_scores.append((k, v, int(dist)))
        print(dist_scores)
        dist_scores = sorted(dist_scores, key=lambda x: x[2],reverse=False)
        return dist_scores[:top_n]



def dist_square(a, b):
    return (b[0] - a[0])**2 + (b[1] - a[1])**2

def make_kd_tree(points, dim, i=0):
    if len(points) > 1:
        points.sort(key=lambda x: x["pos"][i])
        # i dùng để so sánh
        i = (i + 1) % dim
        half = len(points) >> 1
        return [
            make_kd_tree(points[: half], dim, i),
            make_kd_tree(points[half + 1:], dim, i),
            points[half]
        ]
    elif len(points) == 1:
        return [None, None, points[0]]

# Adds a point to the kd-tree
def add_point(kd_tree, point, dim, i=0):
    # dx dùng để lấy j
    dx = kd_tree[2]["pos"][i] >= point["pos"][i]
    # j để vô node trái or phải
    j = (0 if dx else 1)
    # i là dim dùng để so sánh
    i = (i + 1) % dim

    if kd_tree[j] is None:
        kd_tree[j] = [None, None, point]
    else:
        add_point(kd_tree[j], point, dim, i)

# k nearest neighbors
def get_knn(kd_tree, point, k, i=0, heap=None):
    is_root = not heap
    if is_root:
        heap = []
    if kd_tree is not None:
        dist = dist_square(point["pos"], kd_tree[2]["pos"])
        dx = kd_tree[2]["pos"][i] - point["pos"][i]

        if len(heap) < k:
            heapq.heappush(heap, (-dist, kd_tree[2]))
        elif dist < -heap[0][0]:
            heapq.heappushpop(heap, (-dist, kd_tree[2]))
        i = (i + 1) % 2
        # Goes into the left branch, and then the right branch if needed
        for b in [dx < 0] + [dx >= 0] * (dx * dx < -heap[0][0]):
            get_knn(kd_tree[b], point, k, i, heap)
    if is_root:
        neighbors = sorted([-h[0], h[1]] for h in heap)
        return neighbors

# For the closest neighbor
def get_nearest(kd_tree, point, i=0, best=None):
    if kd_tree is not None:
        # Tính khoảng cách giữa 2 điểm
        dist = dist_square(point["pos"], kd_tree[2]["pos"])
        dx = kd_tree[2]["pos"][i] - point["pos"][i]
        # Nếu chưa có best
        if not best:
            best = [dist, kd_tree[2]]
        elif dist < best[0]:
            best[0], best[1] = dist, kd_tree[2]
        
        # i là dim để so sánh
        i = (i + 1) % 2
        # Goes into the left branch, and then the right branch if needed
        for b in [dx < 0] + [dx >= 0] * (dx * dx < best[0]):
            get_nearest(kd_tree[b], point, i, best)
    return best