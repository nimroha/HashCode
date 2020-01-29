import networkx

def point_dist(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])


def ride_distance(ride):
    return point_dist(ride['startPoint'], ride['endPoint'])
