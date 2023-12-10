from collections import deque
from itertools import count
from pathlib import Path
from typing import Literal

HOME = Path(__file__).parent

DIRS = UP,RIGHT,DOWN,LEFT = 0,1,2,3
dir_type = Literal[0,1,2,3] | None

deltas:list[tuple[int,int]] = [(-1,0),(0,1),(1,0),(0,-1)]

dct:dict[
    tuple[int,int,dir_type],
    dir_type] = {} # (y,x,dir) - > dir

tiles = { # where to when coming in with [UP,RIGHT,DOWN,LEFT]?
    "|": [UP,None,DOWN,None],
    "-": [None,RIGHT,None,LEFT],
    "L": [None,None,RIGHT,UP],
    "J": [None,UP,LEFT,None],
    "7": [LEFT,DOWN,None,None],
    "F": [RIGHT,None,None,DOWN],
}

with open(HOME/"input.txt") as f:
    start = None
    for y,line in enumerate(map(str.rstrip,f)):
        for x,c in enumerate(line):
            if c in tiles:
                for d in DIRS: dct[(y,x,d)] = tiles[c][d]
            elif c == "S":
                start = (y,x)
            elif c == ".":
                for d in DIRS: dct[(y,x,d)] = None
    
    assert start is not None
    # try each dir tile
    for letter,tile in tiles.items():
        for d in DIRS: dct[(*start,d)] = tile[d]
        
        for d in DIRS:
            if dct[(*start,d)] is not None:
                break
        else: assert False
        
        y,x = start
        for step in count(1):
            d = dct.get((y,x,d))
            if d is None:
                break
            y += deltas[d][0]
            x += deltas[d][1]
            if (y,x) == start: break
        if d is None:
            print("No path for",letter)
        elif dct[(y,x,d)] is not None:
            print("Path for",letter,step,step//2) # type: ignore
