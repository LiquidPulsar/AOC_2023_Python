from itertools import cycle
import math
from pathlib import Path
import re

HOME = Path(__file__).parent

left = {}
right = {}
sources = []
with open(HOME/"input.txt") as f:
    dirs = f.readline().strip()
    f.readline()
    for k,l,r in re.findall(
        r"(\w+) = \((\w+), (\w+)\)",
        f.read()
        ):
        if k.endswith("A"):
            sources.append(k)
        left[k] = l
        right[k] = r
    
    lcm = 1
    for curr in sources:
        past = {}
        ends = []
        for step,dir in enumerate(cycle(dirs),1):
            # print(step,curr,dir)
            if curr.endswith("Z"):
                ends.append(step)
            p = (curr,(step-1)%len(dirs))
            if p in past: break
            past[p] = step
            curr = right[curr] if dir=='R' else left[curr]
        print(curr,step - past[p],ends)
        lcm = math.lcm(lcm,step - past[p])
    print(lcm)