import pandas as pd
from src.Parser import parseIn,parseOut
from random import randint
import numpy as np


def naive_amitay(streets, n):
    nodes = {i: [name for (name, s) in streets.items() if s['end'] == i] for i in range(n)}
    output = {i: [(s, 1) for s in nodes[i]] for i in range(n)}
    return output

def less_naive_amitay(streets,n,paths, congested=None):
    congested = congested or []
    relevant_streets = set([s.name for l in paths for s in l])
    nodes = {i: [name for (name, s) in streets.items() if s['end'] == i and name in relevant_streets] for i in range(n)}
    output = {}
    for i in range(n):
        output[i] = [(s, 2 if s in congested else 1) for s in nodes[i]]

    return output

def random_naive_amitay(streets,n,paths):
    relevant_streets = set([s.name for l in paths for s in l])
    nodes = {i: [name for (name, s) in streets.items() if s['end'] == i and name in relevant_streets] for i in range(n)}
    output = {i: [(s, randint(1, 3)) for s in nodes[i]] for i in range(n)}
    return output

def get_duration(bins,n):
    if n < bins[0]:
        return 1
    if bins[0] <= n and n < bins[1]:
        return 2
    if bins[1] <= n and n < bins[2]:
        return 3
    if bins[2] <= n and n < bins[3]:
        return 4
    if bins[3] <= n:
        return 5

def freq_naive_amitay(streets,n,paths):
    streets_with_copies = [s.name for l in paths for s in l]
    relevant_streets = set(streets_with_copies)
    streets_freqs = {s: len([a for a in streets_with_copies if a == s]) for s in relevant_streets}
    vals = list(streets_freqs.values())
    bins = np.histogram(vals, 4)[1]
    nodes = {i: [name for (name, s) in streets.items() if s['end'] == i and name in relevant_streets] for i in range(n)}
    output = {i: [(s, get_duration(bins, streets_freqs[s])) for s in nodes[i]] for i in range(n)}
    return output

