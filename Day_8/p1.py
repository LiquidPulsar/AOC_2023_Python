from itertools import cycle
from pathlib import Path
import re

HOME = Path(__file__).parent

dct = {}
with open(HOME/"input.txt") as f:
    dirs = cycle(f.readline().strip())
    f.readline()
    for k,l,r in re.findall(
        r"(\w+) = \((\w+), (\w+)\)",
        f.read()
        ):
        dct[k] = (l,r)

    curr = "AAA"
    for step,dir in enumerate(dirs,1):
        # print(step,curr,dir)
        curr = dct[curr][dir=='R']
        if curr == 'ZZZ':
            print(step)
            break