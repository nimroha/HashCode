from src.Parser import parseIn
from src.Solver import INPUTS


def intersection_load(input):
    streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus = parseIn(INPUTS[input])
    loads = [0] * num_intersections
    for path in paths:
        for edge in path:
            loads[edge.end] += 1
    return loads


def completion_times(input):
    streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus = parseIn(INPUTS[input])
    times = [0] * num_cars
    for car_idx, path in enumerate(paths):
        times[car_idx] = sum([e.duration for e in path])
    return times
