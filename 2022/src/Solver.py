import argparse
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import multiprocess as mp
from random import seed
from random import randint

from sklearn.utils import shuffle
from time import time, sleep
from itertools import compress

from src.Parser import parseIn, parseOut, Data
from src.Utils  import savePickle, loadPickle, validateInputRange


INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'inputs'))
INPUTS    = {k: os.path.join(INPUT_DIR, f'{k}.txt') for k in 'abcefd'}

# seed random number generator
seed(time())

def example_worker(*args):
    print(f'worker {os.getpid()} got {args}')
    sleep(1)
    return randint(0, 100)

def parallelSolve():
    #### SAMPLE PARALLEL CODE ####
    orders = list(range(10))
    numProcs = min(len(orders), os.cpu_count() * 2)
    print(f'using {numProcs} cores')

    with mp.Pool(processes=numProcs) as pool:
        futures = [pool.apply_async(func=example_worker,
                                    args=(order,))
                   for order in orders]

        results = [r.get() for r in futures]
        scores = [p[0] for p in results]

    print(scores)
    bestIdx = np.argmax(scores)
    bestOrder = orders[bestIdx]

    return (bestOrder,) + results[bestIdx]


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

    # TODO solve
    result = None

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
