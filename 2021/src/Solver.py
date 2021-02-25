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

INPUT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, 'inputs')

INPUTS = {'a': os.path.join(INPUT_DIR, 'a.txt'),
          'b': os.path.join(INPUT_DIR, 'b.txt'),
          'c': os.path.join(INPUT_DIR, 'c.txt'),
          'd': os.path.join(INPUT_DIR, 'd.txt'),
          'e': os.path.join(INPUT_DIR, 'e.txt'),
          'f': os.path.join(INPUT_DIR, 'f.txt')}


from random import seed
from random import randint
# seed random number generator
seed(time())
# generate some integers

def sort_books_by_score_j(books_ids, scores):
    """
    take list of books indices and return them ordered by their scores
    :param books_ids:
    :param scores:
    :return: books list ordered by score
    """
    books_scores = np.take(scores, books_ids)
    sorted_books = [book for _, book in sorted(zip(books_scores, books_ids),
                                               key=lambda pair: pair[0],
                                               reverse=True)]
    return np.array(sorted_books)


def remove_scanned_books_j(books_to_check, scanned_books, num_added_books):
    return np.setdiff1d(books_to_check, np.array(scanned_books[:num_added_books]))


def library_max_score_j(library, all_books, days_left, scanned_books=[], num_added_books=0):
    effective_days = days_left - library['signup_time']
    if effective_days <= 0:
        library_sum = -1
    else:
        library_books = library['book_idxs']
        books_to_add = remove_scanned_books_j(library_books, scanned_books, num_added_books)
        sorted_books = sort_books_by_score_j(books_to_add, all_books)
        books_per_day = library['daily_books']
        possible_num_books = books_per_day * effective_days
        if possible_num_books > len(sorted_books):
            num_of_books = len(sorted_books)
        else:
            num_of_books = possible_num_books
        if num_of_books <= 0:
            library_sum = -1
        else:
            books_to_take = sorted_books[:num_of_books]
            library_sum = np.take(all_books, books_to_take).sum()
    return library_sum


#%%
def greedy_book_scanning_j(total_books_num, libraries_num, days_num, book_scores, libraries):
    out = {}
    scanned_libraries = [None for _ in range(libraries_num)]
    scanned_books = [None for _ in range(total_books_num)]
    num_of_libraries_added = 0
    num_of_books_added = 0
    day = 0
    while (day < days_num) and bool(libraries) and len(out) < libraries_num:
        libraries_scores = [library_max_score_j(library,
                                                book_scores,
                                                days_num - day,
                                                scanned_books,
                                                num_of_books_added) for library in libraries]
        # print(libraries_scores)
        library_score_id_pairs = zip(range(len(libraries_scores)), libraries_scores)
        # library_id = np.argmax(np.array(libraries_scores))
        ordered_libraries_by_score = sorted(library_score_id_pairs, key=lambda pair: pair[0])
        library_id = -1
        for library_pair in ordered_libraries_by_score:
            library_id, library_score = library_pair
            if (library_id not in scanned_libraries) and library_score > 0:
                break
        if library_id < 0:
            break
        scanned_libraries[num_of_libraries_added] = library_id
        num_of_libraries_added += 1
        possible_books = libraries[library_id]['book_idxs']
        books_to_add = remove_scanned_books_j(possible_books, scanned_books, num_of_books_added)
        scanned_books[num_of_books_added:num_of_books_added + len(books_to_add)] = books_to_add
        num_of_books_added += len(books_to_add)
        day += libraries[library_id]['signup_time']
        out[library_id] = books_to_add
    out['order'] = scanned_libraries
    return out

def switchSome(order, ratio):
    numSwitches = int(ratio * len(order))
    result = order
    for i in range(numSwitches):
        result = switchOne(result)

    return result

def switchOne(order):
    n = len(order)
    idxA = np.random.randint(0, n)
    idxB = np.random.randint(0, n)
    if idxA == idxB:
        idxB = (idxA + n // 2) % n

    result = order.copy()
    result[idxA] = order[idxB]
    result[idxB] = order[idxA]

    return result



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


def book_scanning_n(total_books_num, libraries_num, days_num, book_scores, libraries):
    initialOrder = shuffle(np.arange(libraries_num))

    for i in range(20):
        orders = [initialOrder] + [switchSome(initialOrder, 0.1) for _ in range(mp.cpu_count() - 1)]
        bestOrder, bestScore, library_scan = parallelSolve(orders, total_books_num, libraries_num, days_num, book_scores, libraries)
        initialOrder = bestOrder
        print(f'generation {i}, best score: {bestScore}')

    return library_scan


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

def solve(inputProblem):
    inPath = os.path.abspath(os.path.join(__file__, INPUTS[inputProblem]))
    personal = ''#'/jona/'
    outPath = inPath + '_result.txt'
    # os.makedirs(outPath + personal, exist_ok=True)
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
