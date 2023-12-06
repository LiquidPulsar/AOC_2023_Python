from dataclasses import dataclass, field
from bisect import insort_left, bisect_right
from pathlib import Path

from more_itertools import chunked

HOME = Path(__file__).parent

def location(seed):
    for _map in maps:
        seed = _map[seed]
    return seed

@dataclass
class RangeMap:
    ranges: list[tuple[int,int,int]] = field(default_factory=list)
    
    def setrange(self,k,v,r): insort_left(self.ranges,(k,v,r))
    
    def __getitem__(self,k):
        i = bisect_right(self.ranges,(k,float("inf"),0))
        if i == 0: return k
        (l,r,d) = self.ranges[i-1]
        return k + d*(l<=k<r)

maps:list[RangeMap] = []
with open(HOME/"input.txt") as f:
    seeds = [*map(int,f.readline().split(": ",1)[1].split())]
    f.readline()
    for part in map(str.splitlines,f.read().split("\n\n")):
        maps.append(RangeMap())
        for line in part[1:]:
            a,b,c = map(int,line.split())
            maps[-1].setrange(b,b+c,a-b) # kl,kr, delta from left to right

    print(min(map(location,seeds)))