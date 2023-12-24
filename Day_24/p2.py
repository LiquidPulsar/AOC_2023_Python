from sympy import Symbol, solve_poly_system
from pathlib import Path
import re

import numpy as np

HOME = Path(__file__).parent
Hailstone = tuple[np.ndarray,np.ndarray]

with open(HOME/"input.txt") as f:
    hailstones = [([*map(int,(a,b,c))],[*map(int,(d,e,f))])
                  for a,b,c,d,e,f in 
                  re.findall(r"(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)",
                             f.read())]

"""
6 unknowns: x,y,z, vx,vy,vz

Each stone introduces one unknown t and solves 3
So need 3?
"""
N = 3

x,y,z,vx,vy,vz = map(Symbol,"x,y,z,vx,vy,vz".split(","))
ts = [Symbol(f"t{i}") for i in range(N)]
equations = []

for t,((hx,hy,hz),(hvx,hvy,hvz)) in zip(ts,hailstones[:N]):
    equations.extend((
        x + vx * t - hx - hvx * t, # type: ignore
        y + vy * t - hy - hvy * t, # type: ignore
        z + vz * t - hz - hvz * t  # type: ignore
    ))

res = solve_poly_system(equations,x,y,z,vx,vy,vz,*ts)
assert res is not None

print(sum(res[0][:3]))