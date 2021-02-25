import argparse
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

from sklearn.utils import shuffle
from time import time

from src.Parser import parseIn, parseOut
from src.Utils  import savePickle, loadPickle



INPUTS = {'a': '../../inputs/a_example.txt',
          'b': '../../inputs/b_read_on.txt',
          'c': '../../inputs/c_incunabula.txt',
          'd': '../../inputs/d_tough_choices.txt',
          'e': '../../inputs/e_so_many_books.txt',
          'f': '../../inputs/f_libraries_of_the_world.txt'}


from random import seed
from random import randint
# seed random number generator
seed(time())
# generate some integers

def sort_books_by_score_j(books_ids, scores):
    books_scores = np.take(scores, books_ids)
    sorted_books = [book for _, book in sorted(zip(books_scores, books_ids),
                                               key=lambda pair: pair[0],
                                               reverse=True)]
    return np.array(sorted_books)


def library_max_score_j(library, all_books, days_left):
    library_books = library['book_idxs']
    sorted_books = sort_books_by_score_j(library_books, all_books)
    books_per_day = library['daily_books']
    possible_num_books = books_per_day * days_left
    if possible_num_books > len(sorted_books):
        num_of_books = len(sorted_books)
    else:
        num_of_books = possible_num_books
    books_to_take = sorted_books[:num_of_books]
    return np.take(all_books, books_to_take).sum()


def switchOne(order):
    idxA = np.random.randint(0, len(order))
    idxB = (idxA + 1) % len(order)
    order[idxA], order[idxB] = order[idxB], order[idxA]

    return order



def book_scanning(*args):
    return None

def book_scanning_g(total_books_num, libraries_num, days_num, book_scores, libraries):
    # libraries = [{'signup_time': 1, 'daily_books': 2, 'book_idxs': np.array([0, 1, 2, 3, 4])}]

    library_scans = {}

    scanned_libraries = [None for i in range(libraries_num)]
    chosen_libraries = [None for i in range(libraries_num)]
    chosen_libraries_num = 0
    scanned_books = [None for i in range(total_books_num)]
    scanned_books_num = 0
    scanned_libraries_num = 0
    while scanned_libraries_num < libraries_num:
        index = randint(0, len(libraries) - 1)
        if index in scanned_libraries:
            continue
        scanned_libraries[scanned_libraries_num] = index
        scanned_libraries_num = scanned_libraries_num + 1

        if libraries[index]['signup_time'] >= days_num:
            continue

        cur_library = libraries[index]
        library_books_ordered = sort_books_by_score_j(cur_library['book_idxs'], book_scores)

        library_books_ordered_unscanned = np.setdiff1d(library_books_ordered,
                                                       np.array(scanned_books[:scanned_books_num]))

        new_days_num = days_num - libraries[index]['signup_time']
        real_scans = min(len(library_books_ordered_unscanned),
                         int(np.float64(cur_library['daily_books']) * np.float64(new_days_num)))
        if real_scans == 0:
            continue

        chosen_libraries[chosen_libraries_num] = index
        chosen_libraries_num = chosen_libraries_num + 1
        library_books_ordered_unscanned_on_time = library_books_ordered_unscanned[:real_scans]

        library_scans[index] = library_books_ordered_unscanned_on_time
        scanned_books[scanned_books_num:scanned_books_num + len(library_books_ordered_unscanned_on_time)] \
            = library_books_ordered_unscanned_on_time
        scanned_books_num = scanned_books_num + len(library_books_ordered_unscanned_on_time)
        days_num = new_days_num

    library_scans["order"] = chosen_libraries[:chosen_libraries_num]

    return library_scans

def get_order_score_y(order, days_left, libraries, books):
    score = 0
    order_suffix = order
    while days_left > 0 and len(order) > 0:
        lib = libraries[order_suffix.pop(0)]
        score += library_max_score_j(lib, books, days_left)
        days_left -= lib['signup_time']

    return score, days_left

def book_scanning_by_order_g(total_books_num, libraries_num, days_num, book_scores, libraries, lib_order):
    # libraries = [{'signup_time': 1, 'daily_books': 2, 'book_idxs': np.array([0, 1, 2, 3, 4])}]

    library_scans = {}

    scanned_libraries = [None for i in range(libraries_num)]
    chosen_libraries = [None for i in range(libraries_num)]
    chosen_libraries_num = 0
    scanned_books = [None for i in range(total_books_num)]
    scanned_books_num = 0
    scanned_libraries_num = 0
    for index in lib_order:
        scanned_libraries[scanned_libraries_num] = index
        scanned_libraries_num = scanned_libraries_num + 1

        if libraries[index]['signup_time'] >= days_num:
            continue

        cur_library = libraries[index]
        library_books_ordered = sort_books_by_score_j(cur_library['book_idxs'], book_scores)

        library_books_ordered_unscanned = np.setdiff1d(library_books_ordered,
                                                       np.array(scanned_books[:scanned_books_num]))

        new_days_num = days_num - libraries[index]['signup_time']
        real_scans = min(len(library_books_ordered_unscanned),
                         int(np.float64(cur_library['daily_books']) * np.float64(new_days_num)))
        if real_scans == 0:
            continue

        chosen_libraries[chosen_libraries_num] = index
        chosen_libraries_num = chosen_libraries_num + 1
        library_books_ordered_unscanned_on_time = library_books_ordered_unscanned[:real_scans]

        library_scans[index] = library_books_ordered_unscanned_on_time
        scanned_books[scanned_books_num:scanned_books_num + len(library_books_ordered_unscanned_on_time)] \
            = library_books_ordered_unscanned_on_time
        scanned_books_num = scanned_books_num + len(library_books_ordered_unscanned_on_time)
        days_num = new_days_num

    library_scans["order"] = chosen_libraries[:chosen_libraries_num]

    return library_scans


def parallelScore(orders, days_num, libraries, books):
    print(orders[0] - orders[1])
    numProcs = len(orders)
    print(f'using {numProcs} cores')

    pool = mp.Pool(processes=numProcs)
    results = [pool.apply_async(func=get_order_score_y,
                                args=(order.tolist(), days_num, libraries, books),)
               for order in orders]
    pool.close()
    pool.join()

    scores = [r.get()[0] for r in results]
    print(scores)
    bestIdx = np.argmax(scores)
    bestOrder = orders[bestIdx]

    return bestOrder


def book_scanning_n(total_books_num, libraries_num, days_num, book_scores, libraries):
    initialOrder = shuffle(np.arange(libraries_num))
    bestOrder = parallelScore([switchOne(initialOrder) for _ in range(2)], days_num, libraries, book_scores)

    return book_scanning_by_order_g(total_books_num, libraries_num, days_num, book_scores, libraries, bestOrder)


def scorer_g(library_scans, total_books_num, libraries_num, days_num, book_scores, libraries):
    score = 0
    for i in range(len(library_scans["order"])):
        lib_idx = library_scans["order"][i]
        if days_num <= libraries[lib_idx]['signup_time']:
            break
        else:
            real_scans = min(len(library_scans[lib_idx]),
                             int(np.float64(libraries[lib_idx]['daily_books']) * np.float64(days_num)))
            score = score + np.sum(np.take(book_scores, library_scans[lib_idx][:real_scans]))
            days_num = days_num - libraries[lib_idx]['signup_time']

    return score

def expected_lib_score_g(cur_library, book_scores, already_scanned_books, days_left):
    signup_time = cur_library["signup_time"]
    if days_left <= signup_time:
        return 0
    library_books_ordered = sort_books_by_score_j(cur_library['book_idxs'], book_scores)

    library_books_ordered_unscanned = np.setdiff1d(library_books_ordered,
                                                   np.array(already_scanned_books))

    days_2_scan = days_left - signup_time
    real_scans = min(len(library_books_ordered_unscanned),
                     int(np.float64(cur_library['daily_books']) * np.float64(days_2_scan)))

    books_scores = np.take(book_scores, library_books_ordered_unscanned[:real_scans])

    return np.sum(books_scores)


def book_scanning_greedy_g(total_books_num, libraries_num, days_num, book_scores, libraries):
    # libraries = [{'signup_time': 1, 'daily_books': 2, 'book_idxs': np.array([0, 1, 2, 3, 4])}]

    library_scans = {}

    scanned_libraries = [None for i in range(libraries_num)]
    chosen_libraries = [None for i in range(libraries_num)]
    chosen_libraries_num = 0
    scanned_books = [None for i in range(total_books_num)]
    scanned_books_num = 0
    scanned_libraries_num = 0
    total_score = 0
    while scanned_libraries_num < libraries_num:

        best_score = -1
        index = None
        for k in range(libraries_num):
            if k in scanned_libraries:
                continue
            # if libraries[k]['signup_time'] >= days_num:
            #     scanned_libraries[scanned_libraries_num] = k
            #     scanned_libraries_num = scanned_libraries_num + 1
            #     continue
            cur_score = expected_lib_score_g(libraries[k], book_scores, scanned_books[:scanned_books_num], days_num)
            if cur_score > best_score:
                best_score = cur_score
                index = k

        if index is None:
            break
        scanned_libraries[scanned_libraries_num] = index
        scanned_libraries_num = scanned_libraries_num + 1

        if libraries[index]['signup_time'] >= days_num:
            continue

        total_score = total_score + best_score
        print("lib score is {} for idx {} with {} days left. Total score is {}".format(best_score, index, days_num, total_score))
        cur_library = libraries[index]
        library_books_ordered = sort_books_by_score_j(cur_library['book_idxs'], book_scores)

        library_books_ordered_unscanned = np.setdiff1d(library_books_ordered,
                                                       np.array(scanned_books[:scanned_books_num]))

        new_days_num = days_num - libraries[index]['signup_time']
        real_scans = min(len(library_books_ordered_unscanned),
                         int(np.float64(cur_library['daily_books']) * np.float64(new_days_num)))
        if real_scans == 0:
            continue

        chosen_libraries[chosen_libraries_num] = index
        chosen_libraries_num = chosen_libraries_num + 1
        library_books_ordered_unscanned_on_time = library_books_ordered_unscanned[:real_scans]

        library_scans[index] = library_books_ordered_unscanned_on_time
        scanned_books[scanned_books_num:scanned_books_num + len(library_books_ordered_unscanned_on_time)] \
            = library_books_ordered_unscanned_on_time
        scanned_books_num = scanned_books_num + len(library_books_ordered_unscanned_on_time)
        days_num = new_days_num

    library_scans["order"] = chosen_libraries[:chosen_libraries_num]

    return library_scans


def solve(inputProblem):
    inPath = os.path.abspath(os.path.join(__file__, INPUTS[inputProblem]))
    outPath = inPath + '_result.txt'
    print(f'Solving {inPath}')

    print("Parsing...")
    if os.path.isfile(inPath + '.pkl'):
        total_books_num, libraries_num, days_num, book_scores, libraries = loadPickle(inPath + '.pkl')
    else:
        total_books_num, libraries_num, days_num, book_scores, libraries = parseIn(inPath)
        savePickle(inPath + '.pkl', (total_books_num, libraries_num, days_num, book_scores, libraries))

    print("Solving...")
    t = time()
    # result = book_scanning_n(total_books_num, libraries_num, days_num, book_scores, libraries)
    result = book_scanning_greedy_g(total_books_num, libraries_num, days_num, book_scores, libraries)
    # print(scorer(result, total_books_num, libraries_num, days_num, book_scores, libraries))
    print(f'problem {inputProblem} took {time() - t:.2f}s')

    # write solution to file
    print("Writing solution to file...")
    # print(f'ordered {np.sum(np.take(pizzas, selected))} of {numSlices} slices')
    try:
        end = result['order'].index(None)
        result['order'] = result['order'][:end]
    except ValueError:
        pass

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
