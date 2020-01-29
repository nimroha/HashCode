import networkx as nx
from networkx import NetworkXNoPath
import matplotlib.pyplot as plt
from src import utils, Parser

class Graph:

    def __init__(self, R, C, T):

        self.end_node = (0,0,T)

        dg = nx.DiGraph()
        for t in range(T):
            for c in range(C):
                for r in range(R):
                    dg.add_node((r, c, t))

        dg.add_node(self.end_node)
        for node in dg.nodes:
            r, c, t = node
            if t < T - 1:

                dg.add_edge(node, (r, c, t + 1), weight=1, label='none')
                if c + 1 < C:
                    dg.add_edge(node, (r, c + 1, t + 1), weight=1, label='none')
                if c > 0:
                    dg.add_edge(node, (r, c - 1, t + 1), weight=1, label='none')
                if r + 1 < R:
                    dg.add_edge(node, (r + 1, c, t + 1), weight=1, label='none')
                if r > 0:
                    dg.add_edge(node, (r - 1, c, t + 1), weight=1, label='none')

            else:
                dg.add_edge(node, self.end_node, weight=0, label='none')

        # nx.draw(dg)
        # plt.show()
        self.dg = dg

    def remove_rides(self, ride_ids):
        for (u,v),label in nx.get_edge_attributes(self.dg, 'label').items():
            if label != 'none' and label in ride_ids:
                self.dg.remove_edge(u, v)

    def find_shortest_path(self):
        try:
            path_of_nodes = nx.dijkstra_path(self.dg, (0,0,0), self.end_node)
            path_of_edges = []
            for i in range(len(path_of_nodes) - 1):
                edge = (path_of_nodes[i], path_of_nodes[i+1])
                path_of_edges.append(self.dg.edges[edge])
        except NetworkXNoPath as e:
            print(e)
            path_of_edges = []

        return path_of_edges


    def add_rides_to_graph(self, rides):
        for ride in rides:
            ride_dist = utils.ride_distance(ride)
            ride_duplications = ride['endTime'] - ride['startTime'] - ride_dist
            for t in range(ride['startTime'], ride['startTime'] + ride_duplications):
                self.dg.add_edge((ride['startPoint'][0], ride['startPoint'][1], t), (ride['endPoint'][0], ride['endPoint'][1], t + ride_dist), weight=-ride_dist, label=ride['rideNum'])
        return self.dg

# rides, R, C, numCars, numRides, bonus, T = Parser.parseIn(r"C:\src\HashCode2018\inputs\a_example.in")
# G = Graph(R,C,T)
# DG = add_rides_to_graph(rides,G.dg)
# nx.draw(DG)
# plt.show()