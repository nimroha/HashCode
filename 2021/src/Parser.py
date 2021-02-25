import numpy as np
import pandas as pd

def readAndSplitLine(fp):
    return [int(x) for x in fp.readline().strip().split()]


def parseIn(path):
    with open(path, 'r') as fp:
        # TODO parse into pandas, not dictionary
        num_steps, num_intersections, num_streets, num_cars, bonus = [int(x) for x in fp.readline().strip().split()]

        streets = {}
        for i in range(num_streets):
            line = fp.readline().strip().split()
            start_i, end_i = int(line[0]), int(line[1])
            name = line[2]
            through_time = int(line[3])
            streets[name] = {'through_time': through_time,
                             'start':        start_i,
                             'end':          end_i}

        paths = [None] * num_cars
        for i in range(num_cars):
            line = fp.readline().strip().split()
            path_length = int(line[0])
            paths[i] = line[:1]

        return streets, paths


def parseOut(path, schedule):

    print(libraries['order'])
    with open(path, 'w') as fp:
        fp.write(f'{len(libraries["order"])}\n')
        for idx in libraries['order']:
            books = libraries[idx]
            if len(books) == 0:
                print(f'WARNING: no books selected for library {idx}')
                continue

            fp.write(f'{idx} {len(books)}\n')
            fp.write(f'{" ".join([str(b) for b in books])}\n')

libraries = {'order': [1, 0],
             1: [5, 2, 3],
             0: [0, 1, 2, 3, 4]}

# parseOut('test.txt', libraries)