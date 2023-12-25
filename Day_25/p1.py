from collections import defaultdict
from pathlib import Path
import networkx as nx

HOME = Path(__file__).parent

with open(HOME/"test.txt") as f:
    dct = defaultdict(list)
    for line in f:
        l,_,r = line.partition(": ")
        for r in r.split():
            dct[l].append(r)
            dct[r].append(l)
    G = nx.Graph(dct)
    n,(l,r) = nx.algorithms.connectivity.stoer_wagner(G)
    assert n == 3
    print(len(l) * len(r))