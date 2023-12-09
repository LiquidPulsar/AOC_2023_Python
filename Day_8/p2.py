from itertools import cycle
from pathlib import Path
import re
import numpy as np

HOME = Path(__file__).parent

left = {}
right = {}
sources = []
targets= []
with open(HOME/"input.txt") as f:
    dirs = cycle(f.readline().strip())
    f.readline()
    names = {}
    n = 0
    for k,l,r in re.findall(
        r"(\w+) = \((\w+), (\w+)\)",
        f.read()
        ):
        for i in (k,l,r):
            if i not in names:
                names[i] = n
                if i.endswith("A"):
                    sources.append(n)
                elif i.endswith("Z"):
                    targets.append(n)
                n += 1
        left[names[k]] = names[l]
        right[names[k]] = names[r]
    
    sources = [i for i in range(n) if i in sources]
    sources = np.array(sources)

    targets = [i for i in range(n) if i in targets]
    targets = np.array(targets)
    
    for step,dir in enumerate(dirs,1):
        # print(step,currs,dir)
        currs = [dct[curr][dir=='R'] for curr in currs]
        if all(c.endswith("Z") for c in currs):
            print(step,time()-t)
            break