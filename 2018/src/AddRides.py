
import src.Graph as Graph
import src.utils as utils

def add_rides_to_graph(rides, graph):
    for ride in rides:
        ride_dist = utils.ride_distance(ride)
        ride_duplications = ride['endTime'] - ride['startTime'] - ride_dist
        for t in range(ride['startTime'],ride['startTime'] + ride_duplications):
            graph.add_edge((ride['startPoint'][0], ride['startPoint'][1], t), (ride['endPoint'][0], ride['endPoint'][1], t + ride_dist), wheight=-ride_dist, label=ride['rideNum'])
    return graph