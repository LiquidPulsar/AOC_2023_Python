from itertools import product
from collections import defaultdict
from pathlib import Path
import re

HOME = Path(__file__).parent



with open(HOME/"input.txt") as f:
    # s[xyz]~e[xyz]
    blocks = [[_id,*map(int,r)] for _id,r in enumerate(re.findall(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)", f.read()))]
    blocks.sort(key=lambda x: x[3])
    # print(blocks)
    supportedby = defaultdict(set)
    supports = defaultdict(set)

    highest = {} # (x,z) -> (y,block_id)
    for i, x1, y1, z1, x2, y2, z2 in blocks:
        h = 0
        sups = []

        for x, y in product(range(x1, x2+1), range(y1, y2+1)):
            old_h,old_id = highest.get((x,y),(0,-1))
            if old_h > h:
                h = old_h
                sups = [old_id]
            elif 0 < h == old_h:
                sups.append(old_id)
        supports[i] = set(sups)
        for s in sups: supportedby[s].add(i)

        for x, y in product(range(x1, x2+1), range(y1, y2+1)):
            highest[x, y] = (h+z2-z1+1,i)
        # print(i,h,highest,sups,(x1, y1, z1, x2, y2, z2))
    # print(supports)

    tot = 0
    for i, *_ in blocks:
        for s in supportedby[i]:
            if len(supports[s]) == 1:
                # print(f"{i} cannot be desintegrated because {s} is supported by {supports[s]}")
                break
        else:
            # print(f"{i} can be desintegrated")
            tot += 1
        # print(i, supports[i], supportedby[i])
    print(tot)