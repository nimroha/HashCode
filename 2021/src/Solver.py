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

from src.Parser import parseIn, parseOut
from src.Utils  import savePickle, loadPickle

INPUT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'inputs')

INPUTS = {k: os.path.join(INPUT_DIR, f'{k}.txt') for k in 'abcdef'}


# seed random number generator
seed(time())
# generate some integers



def worker(lib_order, total_books_num, libraries_num, days_num, book_scores, libraries):
    result = book_scanning_by_order_g(total_books_num, libraries_num, days_num, book_scores, libraries, lib_order)
    score = scorer_g(result, total_books_num, libraries_num, days_num, book_scores, libraries)

    return score, result

def parallelSolve(orders, total_books_num, libraries_num, days_num, book_scores, libraries):
    numProcs = len(orders)
    print(f'using {numProcs} cores')

    pool = mp.Pool(processes=numProcs)
    results = [pool.apply_async(func=worker,
                                args=(order.tolist(), total_books_num, libraries_num, days_num, book_scores, libraries),)
               for order in orders]
    pool.close()
    pool.join()

    results = [r.get() for r in results]
    scores = [p[0] for p in results]
    print(scores)
    bestIdx = np.argmax(scores)
    bestOrder = orders[bestIdx]

    return (bestOrder,) + results[bestIdx]



def solve(inputProblem):
    inPath = INPUTS[inputProblem]
    outPath = inPath + '_result.txt'
    # personal = ''#'/jona/'
    # os.makedirs(outPath + personal, exist_ok=True)
    print(f'Solving {inPath}')

    print("Parsing...")
    if os.path.isfile(inPath + '.pkl'):
        streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus = loadPickle(inPath + '.pkl')
    else:
        streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus = parseIn(inPath)
        savePickle(inPath + '.pkl', (streets, paths, num_steps, num_intersections, num_streets, num_cars, bonus))

    print("Solving...")
    return
    # TODO solve
    t = time()
    # result = book_scanning_n(total_books_num, libraries_num, days_num, book_scores, libraries)
    result = greedy_book_scanning_j(total_books_num, libraries_num, days_num, book_scores, libraries)
    # print(scorer(result, total_books_num, libraries_num, days_num, book_scores, libraries))
    print(f'problem {inputProblem} took {time() - t:.2f}s')

    # write solution to file
    print("Writing solution to file...")
    # print(f'ordered {np.sum(np.take(pizzas, selected))} of {numSlices} slices')
    parseOut(outPath, result)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Solve problem')
    parser.add_argument('-i', '--input', help='Input file id (letter)', default='a', choices=INPUTS.keys())
    parser.add_argument('--loop',        help='run on all inputs',      default=False, action='store_true')
    args = parser.parse_args(argv)

    inputProblem = args.input

    if args.loop:
        for inputProblem in INPUTS.keys():
            solve(inputProblem)
    else:
        solve(inputProblem)

    print("Done")




if __name__ == '__main__' :
    main()
