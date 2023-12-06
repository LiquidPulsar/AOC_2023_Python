from dataclasses import dataclass, field
from bisect import insort_left, bisect_right
from pathlib import Path

from more_itertools import chunked

HOME = Path(__file__).parent

from collections import defaultdict

def location(seed):
    steps = "seed soil fertilizer water light temperature humidity location".split()
    s = iter(steps)
    a = next(s)
    for b in s:
        # print(seed,a,b)
        seed = maps[a][b][seed]
        a = b
        # break
    return seed

@dataclass
class RangeMap:
    ranges: list[tuple[int,int,int]] = field(default_factory=list)
    
    def setrange(self,k,v,r):
        insort_left(self.ranges,(k,v,r))
    
    def __getitem__(self,k):
        i = bisect_right(self.ranges,(k,float("inf"),0))
        # print(self.ranges,(k,0,0),i)
        if i == 0: return k
        (l,v,r) = self.ranges[i-1]
        return v+(k-l) if l<=k<l+r else k

maps = defaultdict(lambda : defaultdict(RangeMap))

with open(HOME/"input.txt") as f:
    seeds = [*map(int,f.readline().split(": ",1)[1].split())]
    f.readline()
    for part in f.read().split("\n\n"):
        part = part.splitlines()
        src,dest = part[0].removesuffix(" map:").split("-to-")
        for line in part[1:]:
            a,b,c = map(int,line.split())
            maps[src][dest].setrange(b,a,c)
    # print(maps["seed"]["soil"])
    print(min(map(location,seeds)))
    # sds = []
    # for l,s in chunked(seeds,2): sds.extend(range(l,l+s))
    # print(sds)
    # print(*map(location,sds))
    # print(min(map(location,sds)))