import argparse
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
from random import seed
from random import randint

from sklearn.utils import shuffle
from time import time
from itertools import compress

from src.Parser import parseIn, parseOut, Data
from src.Utils  import savePickle, loadPickle, validateInputRange
from src.naive_amitay import less_naive_amitay, freq_naive_amitay

INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'inputs'))
INPUTS    = {k: os.path.join(INPUT_DIR, f'{k}.txt') for k in 'abcefd'}

# seed random number generator
seed(time())


def parallelSolve(orders, total_books_num, libraries_num, days_num, book_scores, libraries):
    #### SAMPLE PARALLEL CODE ####
    numProcs = len(orders)
    print(f'using {numProcs} cores')

    pool = mp.Pool(processes=numProcs)
    futures = [pool.apply_async(func=worker,
                                args=(order.tolist(), total_books_num, libraries_num, days_num, book_scores, libraries),)
               for order in orders]
    pool.close()
    pool.join()

    results = [r.get() for r in futures]
    scores = [p[0] for p in results]
    print(scores)
    bestIdx = np.argmax(scores)
    bestOrder = orders[bestIdx]

    return (bestOrder,) + results[bestIdx]


def prune_long_paths(paths, percentile=95):
    lengths = np.array([len(path) for path in paths])
    short_paths = list(compress(paths, lengths <= np.percentile(lengths, percentile)))
    return short_paths


def prune_heavy_paths(paths, percentile=95):
    lengths = np.array([sum([s.duration for s in path]) for path in paths])
    short_paths = list(compress(paths, lengths <= np.percentile(lengths, percentile)))
    return short_paths

def intersection_loads(paths, num_intersections):
    loads = [0] * num_intersections
    for path in paths:
        for edge in path:
            loads[edge.end] += 1

    return loads

def street_loads(streets, num_streets, paths):
    street_enumeration = dict()
    for i, street_name in enumerate(streets.keys()):
        street_enumeration.update({street_name: i})
    loads = {}
    for path in paths:
        for edge in path:
            loads[edge.name] = loads.get(edge.name, 0) + 1

    return loads


def completion_times(input):
    streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus = parseIn(INPUTS[input])
    times = [0] * num_cars
    for car_idx, path in enumerate(paths):
        times[car_idx] = sum([e.duration for e in path])
    return times


def solve(inputProblem, cache_bust=False):
    inPath  = INPUTS[inputProblem]
    outPath = inPath.replace('.txt', '_result.txt')
    print(f'Solving {inPath}')

    print("Parsing...")
    if os.path.isfile(inPath + '.pkl') and not cache_bust:
        data = loadPickle(inPath + '.pkl')
    else:
        data = parseIn(inPath)
        savePickle(inPath + '.pkl', data)

    print("Solving...")
    print(f'{inputProblem}: bonus * num_cars = {data.bonus * data.num_cars}')
    t = time()

    # data.paths = prune_heavy_paths(data.paths, percentile=80)
    loads = intersection_loads(data.paths, data.num_intersections)
    loads = street_loads(data.streets, data.num_streets, data.paths)
    thresh = np.percentile([v for v in loads.values()], 90)
    congested = [k for k, v in loads.items() if v >= thresh]
    result = less_naive_amitay(data.streets, data.num_intersections, data.paths, congested=congested)
    # result = freq_naive_amitay(data.streets, data.num_intersections, data.paths)
    print(f'problem {inputProblem} took {time() - t:.2f}s')

    # write solution to file
    print("Writing solution to file...")
    parseOut(outPath, result)





def main(argv=None):
    parser = argparse.ArgumentParser(description='Solve problem')
    parser.add_argument('-i', '--input', help='Input file letter(s)', default='a', type=validateInputRange(''.join(INPUTS.keys())))
    parser.add_argument('--cache_bust',  help='rerun parser',         default=False, action='store_true')
    args = parser.parse_args(argv)

    inputProblems = args.input
    for problem in inputProblems:
        solve(problem, args.cache_bust)

    print("Done")




if __name__ == '__main__' :
    main()
