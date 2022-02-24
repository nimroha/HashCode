import numpy as np
import matplotlib.pyplot as plt
import pickle

from argparse import ArgumentTypeError

def plotHist(lst, title):
    max = np.max(lst)
    min = np.min(lst)
    plt.hist(lst, np.arange(start=min, stop=max))
    plt.title(title)
    plt.show()


def savePickle(savePath, obj):
    """
    pickle dump wrapper

    :param savePath: path to save
    :param obj: object to save
    """
    with open(savePath, 'wb') as fp:
        pickle.dump(obj, fp)


def loadPickle(loadPath):
    """
    pickle load wrapper

    :param loadPath: path to load

    :return: python object
    """
    with open(loadPath, 'rb') as fp:
        return pickle.load(fp)


def validateInputRange(valid):
    """
    validate the input problem arg is valid

    :param valid: list of valid problem inputs

    :return: the argument if it's valid
    :raise ArgumentTypeError: if it's not valid
    """
    def func(arg):
        if (not isinstance(arg, str) or
            len(set(arg) - set(valid)) > 0):
            raise ArgumentTypeError(f'input argument must be any subset (in any order) of "{valid}", got "{arg}"')

        return arg

    return func
