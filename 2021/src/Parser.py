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
            streets[name] = {'duration': through_time,
                             'start':    start_i,
                             'end':      end_i}

        paths = [None] * num_cars
        for i in range(num_cars):
            line = fp.readline().strip().split()
            path_length = int(line[0])
            paths[i] = line[:1]

        return streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus


def parseOut(path, schedules):
    with open(path, 'w') as fp:
        fp.write(f'{len(schedules)}\n')
        for intersection, schedule in schedules.items():
            fp.write(f'{intersection}\n')
            fp.write(f'{len(schedule)}\n')
            for name, duration in schedule:
                fp.write(f'{name} {duration}\n')

# parseIn('test.txt')
# parseOut('test.txt', libraries)