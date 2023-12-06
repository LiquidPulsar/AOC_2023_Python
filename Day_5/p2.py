from itertools import starmap, chain
from functools import reduce
from dataclasses import dataclass, field
from bisect import insort_left, bisect_right
from pathlib import Path

INF = int(1e10)
HOME = Path(__file__).parent

@dataclass
class RangeMap:
    # kleft,kright,delta | kright exclusive
    ranges: list[tuple[int,int,int]] = field(default_factory=list)
    
    def setrange(self,kl,kr,vl): insort_left(self.ranges,(kl,kr,vl))

    def get_overlaps(self,kl,kr) -> list[tuple[int,int]]:
        assert kr>kl

        i = bisect_right(self.ranges,(kl,float('inf'),0))
        (_,prv_kr,prv_d) = self.ranges[i-1] if i else (-INF,-INF,0)
        if prv_kr<=kl:
            if i == len(self.ranges): return [(kl,kr)] # off the right side
            nxt_kl = self.ranges[i][0]
            return (
                [(kl, kr)]
                if nxt_kl >= kr
                else [(kl, nxt_kl)] + self.get_overlaps(nxt_kl, kr)
            )

        if prv_kr<kr: # prv_kl known <= kl
            return [translate((kl,prv_kr),prv_d)] + self.get_overlaps(prv_kr,kr)
        else:
            return [translate((kl,kr),prv_d)]
    
def translate(ab:tuple[int,int],c:int) -> tuple[int,int]:
    return (ab[0]+c,ab[1]+c)

def pipeline(lst:list[tuple[int,int]],_map:RangeMap):
    return chain.from_iterable(starmap(_map.get_overlaps, lst))

def locations(seeds:list[tuple[int,int]]):
    return reduce(pipeline,maps,seeds) # type: ignore


maps:list[RangeMap] = []
with open(HOME/"input.txt") as f:
    seeds = [*map(int,f.readline().split(": ",1)[1].split())]
    f.readline()
    for part in map(str.splitlines,f.read().split("\n\n")):
        maps.append(RangeMap())
        for line in part[1:]:
            a,b,c = map(int,line.split())
            maps[-1].setrange(b,b+c,a-b) # kl,kr, delta from left to right

    print(min(map(lambda x: x[0],locations([(l,l+s) for l,s in zip(seeds[::2],seeds[1::2])]))))