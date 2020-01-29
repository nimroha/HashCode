
import numpy as np


def parseIn(path):
    with open(path, 'r') as f:
        rows, cols, numCars, numRides, bonus, maxTime = f.readline().strip().split()
        rides = []
        for line in f:
            a, b, x, y, s, f = line.strip().split()
            rides.append({'startPoint' : (int(a), int(b)),
                          'endPoint'   : (int(x), int(y)),
                          'startTime'  : int(s),
                          'endTime'    : int(f),
                          'rideNum'    : len(rides)})

    return rides, int(rows), int(cols), int(numCars), int(numRides), int(bonus), int(maxTime)

def parseOut(path, schedule):
    with open(path, 'w') as f:
        for car in schedule:
            f.write('{numRides} {rideIds}\n'.format(numRides=len(car), rideIds=' '.join(str(id) for id in car)))

