import numpy as np
import matplotlib.pyplot as plt
import pickle


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

    :param loadPath: peth to load

    :return: python object
    """
    with open(loadPath, 'rb') as fp:
        return pickle.load(fp)
