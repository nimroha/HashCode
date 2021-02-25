import numpy as np

def parseIn(path):
    with open(path, 'r') as fp:
        line = np.array([int(x) for x in fp.readline().strip().split()])
        total_books_num, libraries_num, days_num = (line[i] for i in range(3))
        book_scores = np.array([int(x) for x in fp.readline().strip().split()])
        libraries = []
        for i in range(libraries_num):
            library = {}
            line = np.array([int(x) for x in fp.readline().strip().split()])
            books_num, signup_time, daily_books = (line[k] for k in range(3))
            library["books_num"] = books_num
            library["signup_time"] = signup_time
            library["daily_books"] = daily_books
            library["book_idxs"] = np.array([int(x) for x in fp.readline().strip().split()])
            libraries.append(library)

    return total_books_num, libraries_num, days_num, book_scores, libraries


def parseOut(path, libraries):
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