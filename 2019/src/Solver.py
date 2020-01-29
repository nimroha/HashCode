import sys
import argparse
import os
import pickle
import matplotlib.pyplot as plt

import numpy as np

from sklearn.utils import shuffle

INPUTS = {'a': '../inputs/a_example.txt',
          'b': '../inputs/b_lovely_landscapes.txt',
          'c': '../inputs/c_memorable_moments.txt',
          'd': '../inputs/d_pet_pictures.txt',
          'e': '../inputs/e_shiny_selfies.txt'}


def parseIn(path):
    with open(path, 'r') as fp:
        numPhotos = int(fp.readline().strip().split()[0])
        photos    = []
        for line in fp:
            orientation, numTags, *tags = line.strip().split()
            photos.append({'orient':  orientation,
                           'numTags': int(numTags),
                           'tags':    tags,
                           'id':      str(len(photos))})

    return numPhotos, photos

def parseOut(path, slideshow):
    print(slideshow)
    with open(path, 'w') as fp:
        fp.write('{}\n'.format(len(slideshow)))
        [fp.write('{}\n'.format(slide)) for slide in slideshow]


def plotHist(lst, title):
    max = np.max(lst)
    min = np.min(lst)
    plt.hist(lst, np.arange(start=min, stop=max))
    plt.title(title)
    plt.show()


def oneHotRun(photos):
    words = {}
    for photo in photos:
        for tag in photo["tags"]:
            if tag not in words:
                words[tag] = {
                    "idx": len(words),
                    "amount": 1
                }
            else:
                words[tag]['amount'] += 1

    return words


def addOneHots2Photos(photos):
    words = oneHotRun(photos)
    for i in range(len(photos)):
        photos[i]["oneHot"] = np.zeros(len(words))
        for tag in photos[i]["tags"]:
            photos[i]["oneHot"][words[tag]["idx"]] += 1

    return words

def matchVerticals(photos):
    pass #TODO

def vertConnect(verticals):
    i = 0
    while i < len(verticals):
        j = i + 1
        foundBest = 0
        bestCommonTags = np.Inf
        if i == len(verticals)-1:
            del verticals[i]
            return verticals
        while j < len(verticals):
            commonTags = np.sum(np.logical_and(verticals[i]["oneHot"], verticals[j]["oneHot"]).astype(int))
            # print("i: {}, j: {}, commonTags: {}, len(verts): {}".format(i, j, commonTags, len(verticals)))
            if commonTags == 0:
                verticals[i]["oneHot"] = np.logical_or(verticals[i]["oneHot"], verticals[j]["oneHot"]).astype(int)
                verticals[i]["id"] = verticals[i]["id"] + " " + verticals[j]["id"]
                verticals[i]["numTags"] = verticals[i]["numTags"] + verticals[j]["numTags"]
                del verticals[j]
                foundBest = 1
                break
            elif commonTags < bestCommonTags:
                BestJ = j
            j += 1
        if not foundBest:
            verticals[i]["oneHot"] = np.logical_or(verticals[i]["oneHot"], verticals[BestJ]["oneHot"]).astype(int)
            verticals[i]["id"] = verticals[i]["id"] + " " + verticals[BestJ]["id"]
            verticals[i]["numTags"] = np.sum(verticals[i]["oneHot"])
            del verticals[BestJ]
        i += 1

    return verticals

def solveB(photos, startIdx=None):
    chosen  = np.zeros(shape=len(photos))
    currIdx = startIdx or np.random.randint(0, len(photos))
    slides  = [currIdx]
    chosen[currIdx] = 1
    while np.sum(chosen) < len(photos):
        for i in range(len(photos)):
            if i != currIdx and \
               not chosen[i] and \
               np.sum(np.logical_and(photos[currIdx]['oneHot'], photos[i]['oneHot'])) > 0:
                slides.append(i)
                currIdx   = i
                chosen[i] = 1

        notChosen = np.squeeze(np.argwhere(chosen == 0))

        if len(notChosen) == 0:
            break

        # currIdx = np.random.choice(notChosen) # start fresh from not chosen
        currIdx = np.min(notChosen)
        slides.append(currIdx)
        chosen[currIdx] = 1

    return slides


def solveNotB(photos):
    diff      = 2
    lenSelect = photos[0]['numTags'] - diff
    subPhotos = np.array([p for p in photos if lenSelect - diff <= p['numTags'] <= lenSelect + diff])

    currIdx = np.random.randint(0, len(subPhotos))

    return slides


def main(argv=None):

    parser = argparse.ArgumentParser(description='Solve problem')

    parser.add_argument('--i', help='Path to input file.', required=True)

    args = parser.parse_args(argv)

    inPath  = INPUTS[args.i]
    outPath = os.path.splitext(inPath)[0] + '_result.txt'


    print("Parsing...")
    numPhotos, photos = parseIn(inPath)
    photos.sort(key=lambda p: p['numTags'], reverse=True)
    print('hi')
    words = addOneHots2Photos(photos) #adds onehots to photos
    print('parsed words')
    verticals = [p for p in photos if p['orient'] == 'V']
    horizs = [p for p in photos if p['orient'] == 'H']

    ids = ['{} {}'.format(verticals[i]['id'], verticals[i+1]['id']) for i in range(0, len(verticals) - 1, 2)]
    ids += [p['id'] for p in horizs]

    connected = vertConnect(verticals)

    both    = horizs + connected

    # with open(os.path.splitext(inPath)[0] + '_horiz_only', 'wb') as fp:
    #     pickle.dump(horizs, fp, pickle.HIGHEST_PROTOCOL)

    # plotHist([w['amount'] for w in words.values()], 'Word occurences')
    # plotHist([p['numTags'] for p in photos], 'Number of tags per photo')

    print("Solving...")
    if args.i == 'b':
        slides = solveB(both, startIdx=0)
    else:
        slides = solveNotB(both)

    print(slides)

    # write solution to file
    print("Writing solution to file...")
    slideshow = [photos[i]['id'] for i in slides]
    parseOut(outPath, slideshow)

    print("Done")


if __name__ == '__main__' :
    sys.exit(main())
