import numpy as np

def parseIn(path):
    with open(path, 'r') as fp:
        numSlices = int(fp.readline().strip().split()[0])
        pizzas = np.array([int(x) for x in fp.readline().strip().split()])
        # for i, line in enumerate(fp):
        #     orientation, numTags, *tags = line.strip().split()
        #     photos.append({'orient':  orientation,
        #                  'numTags': int(numTags),
        #                  'tags':    tags,
        #                  'id':      str(len(photos))})

    return numSlices, pizzas

def parseOut(path, pizzas):
    print(pizzas)
    with open(path, 'w') as fp:
        fp.write(f'{len(pizzas)}\n')
        [fp.write(f'{p} ') for p in pizzas]
        fp.write('\n')
