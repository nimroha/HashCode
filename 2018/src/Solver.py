
import sys
import argparse

from src.Parser import parseIn, parseOut
from src.Graph import Graph

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser(description='Solve car sharing problem')

    parser.add_argument('--input',   help='Path to input file.', required=True)
    parser.add_argument('--output',  help='Path to output file', required=True)

    args = parser.parse_args()
    inPath  = args.input
    outPath = args.output

    print("Parsing...")
    rides, rows, cols, numCars, numRides, bonus, maxTime = parseIn(inPath)
    print("numCars: {n}, numRides: {m}, gridSize: ({y},{x}), totalTime: {t}".format(n=numCars,
                                                                                    m=numRides,
                                                                                    x=cols,
                                                                                    y=rows,
                                                                                    t=maxTime))
    print("Solving...")
    # build graph
    graph = Graph(rows, cols, maxTime)

    # add weights
    graph.add_rides_to_graph(rides)

    # build schedule greedily (car by car)
    schedule = []
    for car in range(numCars):
        edges = graph.find_shortest_path()
        print(edges)
        ridesTaken = []
        for edge in edges:
            if edge['label'] != 'none':
                ridesTaken.append(edge['label'])
        ridesTaken.sort()
        print("Taken rides: ", ridesTaken)
        schedule.append(ridesTaken)
        graph.remove_rides(ridesTaken)

    # write solution to file
    print("Writing solution to file...")
    parseOut(outPath, schedule)

    print("Done")


if __name__ == '__main__' :
    sys.exit(main())
