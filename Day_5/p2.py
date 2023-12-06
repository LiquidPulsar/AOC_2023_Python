from dataclasses import dataclass, field
from bisect import insort_left, bisect_right
from more_itertools import chunked
from pathlib import Path

HOME = Path(__file__).parent

from collections import defaultdict

steps = "seed soil fertilizer water light temperature humidity location".split()

def locations(seeds):
    s = iter(steps)
    a = next(s)
    for b in s:
        nxt_seeds = []
        for seed in seeds:
            nxt_seeds.extend(maps[a][b].checked(*seed))
        seeds = nxt_seeds
        a = b
    return seeds

@dataclass
class RangeMap:
    # kleft,kright,vleft | kright exclusive
    ranges: list[tuple[int,int,int]] = field(default_factory=list)
    
    def setrange(self,kl,kr,vl):
        insort_left(self.ranges,(kl,kr,vl))
    
    def find_left(self,k):
        return bisect_right(self.ranges,(k,float('inf'),0))

    def get_overlaps(self,kl,kr):
        assert kr>kl
        if not self.ranges: return [(kl,kr)] # Nothing to overlap
        i = self.find_left(kl)
        (_,prv_kr,prv_d) = self.ranges[i-1] if i else (float('-inf'),float('-inf'),0)
        if prv_kr<=kl:
            if i == len(self.ranges): return [(kl,kr)] # off the right side
            nxt_kl = self.ranges[i][0]
            return (
                [(kl, kr)]
                if nxt_kl >= kr
                else [(kl, nxt_kl)] + self.get_overlaps(nxt_kl, kr)
            )
        # prv_kl known <= kl

        if prv_kr<kr:
            return [translate((kl,prv_kr),prv_d)] + self.get_overlaps(prv_kr,kr)
        else:
            return [translate((kl,kr),prv_d)]
    
    def checked(self,kl,kr):
        res = self.get_overlaps(kl,kr)
        res2 = self.worse([(kl,kr)])
        if set(res) != set(res2):
            print("========== ERROR ==========")
            print(kl,kr,self.ranges)
            print("res",res)
            print("res2",res2)
            print(set(res) - set(res2))
            print(set(res2) - set(res))
        assert set(res) == set(res2), f'{set(res) - set(res2)} {set(res2) - set(res)}'
        return res

    
    def worse(self,seeds):
        seeds = seeds.copy()
        out = []
        while seeds:
            s, e = seeds.pop()
            for kl,kr,d in self.ranges:
                ll = max(kl,s)
                rr = min(kr,e)
                if ll<rr:
                    out.append((ll+d,rr+d))
                    if s < ll:
                        seeds.append((s,ll))
                    if rr < e:
                        seeds.append((rr,e))
                    break
            else:
                out.append((s,e))
        return out

def translate(ab,c):
    (a,b) = ab
    return (a+c,b+c)

# m = RangeMap()

# m.setrange(0,37,15)
# m.setrange(37,39,52)
# m.setrange(39,54,0)

# print(m.get_overlaps(-1,0))

def fails(l,r):
    try:
        maps["seed"]["soil"].checked(l,r)
        return False
    except AssertionError:
        print("Failed",l,r)
        return True

maps = defaultdict(lambda : defaultdict(RangeMap))

with open(HOME/"input.txt") as f:
    seeds = [*map(int,f.readline().split(": ",1)[1].split())]
    f.readline()
    for part in f.read().split("\n\n"):
        part = part.splitlines()
        src,dest = part[0].removesuffix(" map:").split("-to-")
        for line in part[1:]:
            a,b,c = map(int,line.split())
            maps[src][dest].setrange(b,b+c,a-b) # kl,kr, delta from left to right
    
    # l,r = 635790399,1341769649
    # gap = r-l
    # while gap:
    #     print(l,r,gap)
    #     gap //= 2
    #     if fails(l+gap,r):
    #         l += gap
    #     elif fails(l,r-gap):
    #         r -= gap
    #     else:
    #         print("ERROR")
    #         break

    # 768672890 768672903
    # (629314747, 762725199, -360088562), (768672891, 808199470, 2401051598)

    # print(maps["seed"]["soil"].ranges)
    # maps["seed"]["soil"].checked(768672890, 768672903)

    # print(maps["soil"]["fertilizer"])
    # RangeMap(ranges=[(0, 37, 15), (37, 39, 52), (39, 54, 0)])
    # print(maps["soil"]["fertilizer"].get_overlaps(53,67))
    # print(min(map(location,seeds)))
    # print([(l,l+s) for l,s in chunked(seeds,2)])
    res = locations([(l,l+s) for l,s in chunked(seeds,2)])
    # print(res)
    print(min(map(lambda x: x[0],res)))
    # print(sorted(res,key=lambda x: x[0]))