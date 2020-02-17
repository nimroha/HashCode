import argparse
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np

from sklearn.utils import shuffle
from time import time

from src.Parser import parseIn, parseOut
from src.Utils  import savePickle, loadPickle


INPUTS = {'a': '../../inputs/a_example.in',
          'b': '../../inputs/b_small.in',
          'c': '../../inputs/c_medium.in',
          'd': '../../inputs/d_quite_big.in',
          'e': '../../inputs/e_also_big.in'}


from random import seed
from random import randint
# seed random number generator
seed(time())
# generate some integers

def random_pizza(slices, pizzas):
    # num_of_pizzas = len(pizzas)
    chosen_pizzas = []
    chosen_pizzas_idxs = []
    used_indexes = []
    index = randint(0, len(pizzas)-1)
    while index not in used_indexes and \
            np.sum(chosen_pizzas) + pizzas[index] < slices:
        chosen_pizzas.append(pizzas[index])
        chosen_pizzas_idxs.append(index)
        used_indexes.append(index)
        index = randint(0, len(pizzas)-1)

    return np.sort(chosen_pizzas_idxs), np.sum(chosen_pizzas)


def random_pizza_smarter(slices, pizzas):
    # num_of_pizzas = len(pizzas)
    chosen_pizzas = []
    chosen_pizzas_idxs = []
    used_indexes = []
    while len(pizzas) > len(used_indexes):
        index = randint(0, len(pizzas)-1)
        if index not in used_indexes and \
                np.sum(chosen_pizzas) + pizzas[index] < slices:
            chosen_pizzas.append(pizzas[index])
            chosen_pizzas_idxs.append(index)
        used_indexes.append(index)

    return np.sort(chosen_pizzas_idxs), np.sum(chosen_pizzas)


def random_pizza_master(slices, pizzas, rounds):
    best_num = 0
    best = []
    for i in range(rounds):
        chosen_pizzas, round_sum = random_pizza_smarter(slices, pizzas)
        if round_sum > best_num:
            best_num = round_sum
            best = chosen_pizzas

    return best


def solve(inputProblem):
    inPath = os.path.abspath(os.path.join(__file__, INPUTS[inputProblem]))
    outPath = inPath + '_result.txt'
    print(f'Solving {inPath}')

    print("Parsing...")
    if os.path.isfile(inPath + '.pkl'):
        numSlices, pizzas = loadPickle(inPath + '.pkl')
    else:
        numSlices, pizzas = parseIn(inPath)
        savePickle(inPath + '.pkl', (numSlices, pizzas))

    print("Solving...")
    selected = random_pizza_master(numSlices, pizzas, 10000)

    # write solution to file
    print("Writing solution to file...")
    print(f'ordered {np.sum(np.take(pizzas, selected))} of {numSlices} slices')
    parseOut(outPath, selected)


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
