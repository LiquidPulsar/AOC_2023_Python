from pathlib import Path
import re
from typing import List
from sys import setrecursionlimit
setrecursionlimit(1_000_000)

HOME = Path(__file__).parent

moves = {
    "U": -1j,
    "D": 1j,
    "L": -1,
    "R": 1,
}

with open(HOME/"input.txt") as f:
    dig:dict[complex,list[int|None]] = {} # pos: color
    edges_dug = 0
    pos = 0j
    minx = miny = float("inf")
    maxx = maxy = float("-inf")
    for dir,length,col in re.findall(r"([UDLR]) (\d+) \(#(\w+)\)",f.read()):
        length = int(length)
        col = int(col,16)
        edges_dug += length
        for _ in range(length):
            l = dig.setdefault(pos,[None]*4)
            if dir in "LR":
                l[0] = l[2] = col
            else:
                l[1] = l[3] = col
            pos += moves[dir]
        minx = min(minx,pos.real)
        miny = min(miny,pos.imag)
        maxx = max(maxx,pos.real)
        maxy = max(maxy,pos.imag)

    # for y in range(int(miny),int(maxy)+1):
    #     pos = complex(minx,y)
    #     for _ in range(int(minx),int(maxx)+1):
    #         if pos in dig:
    #             print(end="#")
    #         else:
    #             print(end=".")
    #         pos += 1
    #     print()
    
    def floodfill(pos: complex, dig: dict[complex, List[int|None]], seen: dict[complex,bool], lagoon: list[int]) -> bool:
        if pos.real < minx or pos.real > maxx or pos.imag < miny or pos.imag > maxy:
            # print(pos,False,"Out of bounds")
            return False
        if pos in seen:
            # print(pos,True, "seen")
            return seen[pos]
        seen[pos] = True
        if pos in dig:
            # print(pos,True, "dug")
            return True
        lagoon[0] += 1
        for move in moves.values():
            r = floodfill(pos + move, dig, seen, lagoon)
            # print(pos,r,"Trying",pos+move)
            if not r:
                seen[pos] = False
                return False
        # print(pos,True,"Succeeded")
        return True
        # return all(floodfill(pos + move, dig, seen, lagoon) for move in moves.values())

    seen = {}
    for y in range(int(miny),int(maxy)+1):
        pos = complex(minx,y)
        for _ in range(int(minx),int(maxx)+1):
            if pos not in dig and pos not in seen:
                res = [0]
                if floodfill(pos,dig,seen,res):
                    print(res[0]+edges_dug)
            pos += 1
