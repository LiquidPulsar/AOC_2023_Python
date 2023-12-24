from pathlib import Path
from tqdm import tqdm
import re

import numpy as np

HOME = Path(__file__).parent
Hailstone = tuple[np.ndarray,np.ndarray]

with open(HOME/"input.txt") as f:
    hailstones = [(np.array([*map(int,(a,b))]), np.array([*map(int,(d,e))])) for a,b,c,d,e,f in re.findall(r"(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)",f.read())]
# inclusive
# MIN, MAX = 7, 27
MIN, MAX = 200000000000000, 400000000000000

def collide(a:Hailstone,b:Hailstone) -> np.ndarray | None:
    s1,v1 = a
    s2,v2 = b

    """
    s1 + t*v1 = s2 + u*v2
    s1 - s2 = u*v2 - t*v1
    """
    if np.linalg.det(np.column_stack((v1,v2))):
        u,t = np.linalg.inv(np.column_stack((v1,v2))) @ (s1 - s2) # type: ignore
        np.testing.assert_allclose(s1 - u*v1, s2 + t*v2)
        if t < 0 or u > 0:
            # print("crossed in the past")
            return None # only consider future

        return s2 + t*v2
    # print("parallel")
    return None


tot = 0
for i,h1 in tqdm(enumerate(hailstones),total=len(hailstones)):
    for h2 in hailstones[i+1:]:
        if (res := collide(h1,h2)) is not None:
            x,y = res
            if MIN<=x<+MAX and MIN<=y<+MAX:
                tot += 1
                # print("Cross inside",h1,h2,res)
            # else:
                # print("outside")
print(tot)