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

from Parser import parseIn, parseOut
from Utils  import savePickle, loadPickle, validateInputRange

import guy
import jonathan
import nimrod
import yair
import amitay


INPUT_DIR   = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'inputs'))
INPUT_FILES = os.listdir(INPUT_DIR)
INPUTS      = {f[0]: os.path.join(INPUT_DIR, f) for f in INPUT_FILES}

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
    dir_name, file_name = os.path.split(inPath)
    outPath = os.path.join(dir_name, f'result_{file_name}')
    print(f'Solving {inPath}')

    print("Parsing...")
    people, projects, all_skills = parseIn(inPath)

    print("Solving...")
    t = time()

    # TODO solve
    plan = amitay.solve(people,projects)

    print(f'problem {inputProblem} took {time() - t:.2f}s')

    # write solution to file
    print("Writing solution to file...")
    parseOut(outPath, plan)



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
