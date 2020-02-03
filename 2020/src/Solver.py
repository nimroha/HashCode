import argparse
import os
import pickle
import matplotlib.pyplot as plt
import numpy as np

from sklearn.utils import shuffle

from src.Parser import parseIn, parseOut
from src.Utils  import savePickle, loadPickle


INPUTS = {'a': '../inputs/a_example',
          'b': '../inputs/b_lovely_landscapes',
          'c': '../inputs/c_memorable_moments',
          'd': '../inputs/d_pet_pictures',
          'e': '../inputs/e_shiny_selfies'}


def main(argv=None):

    parser = argparse.ArgumentParser(description='Solve problem')
    parser.add_argument('--i', help='Input file id (letter)', required=True)
    args = parser.parse_args(argv)

    inPath  = INPUTS[args.i]
    outPath = inPath + '_result.txt'

    print("Parsing...")
    if os.path.isfile(inPath + '.pkl'):
        numPhotos, photos = loadPickle(inPath + '.pkl')
    else:
        numPhotos, photos = parseIn(inPath)
        savePickle(inPath + '.pkl', (numPhotos, photos))

    print("Solving...")
    # TODO

    # write solution to file
    print("Writing solution to file...")
    parseOut(outPath, None)

    print("Done")


if __name__ == '__main__' :
    main()
