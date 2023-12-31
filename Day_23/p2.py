from dataclasses import dataclass
from pathlib import Path
from colorama import Fore, Style
import numpy as np
from numba import njit
from numba.typed import Dict
from numba.core import types

from time import time
_t = time()

HOME = Path(__file__).parent
NINF = int(-1e9)

with open(HOME/"input.txt") as f: board = [list(l.rstrip()) for l in f]
W,H = len(board[0]), len(board)

def print_board():
    print()
    for l in board: print(*l,sep="")

# print_board()

# Represent section by start, end, length, exits on each end
# (not generalised but from observation)

Coord = tuple[int,int]

@dataclass
class Section:
    id: int
    start: Coord
    end: Coord
    length: int
    s_exits: list[Coord]
    e_exits: list[Coord]

    @classmethod
    def from_search(cls,id,y,x,seen):
        s,e,l = find_ends(y,x,seen)
        s,e = sorted((s,e)) # just to have the start be smaller
        return cls(
            id,s,e,l,exits(*s),exits(*e)
        )

    def exits_from(self, coord: Coord):
        assert coord in (self.start,self.end)
        return self.e_exits if coord == self.start else self.s_exits
    
    def gen_path(self):
        curr = self.start
        seen = set()
        while curr != self.end:
            seen.add(curr)
            yield curr
            for y,x in neighs(*curr):
                if (y,x) not in seen and unhighlighted(board[y][x]) == ".":
                    curr = (y,x)
                    break
            else:
                assert False
        yield curr

    # Wrecks the board
    def highlight(self,color=Fore.GREEN,exit_color=Fore.BLUE):
        for y,x in self.gen_path(): highlight(y,x,color)

        ey,ex = self.start
        for y,x in self.s_exits:
            highlight(ey + (y-ey)//2, ex + (x-ex)//2, exit_color)

        ey,ex = self.end
        for y,x in self.e_exits:
            highlight(ey + (y-ey)//2, ex + (x-ex)//2, exit_color)
    

    def unhighlight(self):
        for y,x in self.gen_path(): unhighlight(y,x)

        ey,ex = self.start
        for y,x in self.s_exits:
            unhighlight(ey + (y-ey)//2, ex + (x-ex)//2)

        ey,ex = self.end
        for y,x in self.e_exits:
            unhighlight(ey + (y-ey)//2, ex + (x-ex)//2)


def highlight(y,x,color):
    board[y][x] = color + board[y][x] + Style.RESET_ALL

def unhighlight(y,x):
    # can already be unhighlighted (singleton section had start_exits and end_exits duplicated)
    board[y][x] = unhighlighted(board[y][x])

def unhighlighted(s:str):
    # if "m" not in board[y][x]: return board[y][x]
    return s.strip("\x1b[0123456789m")


def neighs(y,x):
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        ny,nx = y+dy,x+dx
        if 0<=ny<H and 0<=nx<W:
            yield ny,nx

def see(y,x,seen): seen.add((y,x))

def unsee(y,x,seen): seen.remove((y,x))

def find_end(y,x,seen) -> tuple[Coord,int]:
    see(y,x,seen)
    for ny,nx in neighs(y,x):
        if (ny,nx) not in seen and board[ny][nx] == ".":
            c,l = find_end(ny,nx,seen)
            return c,l+1
    return (y,x),1

def exits(y,x) -> list[Coord]:
    # Walk an additional step: ny + (ny-y) etc
    return [(ny*2-y,nx*2-x) for ny,nx in neighs(y,x) if
        board[ny][nx] in "><^v"]

def find_ends(y,x,seen) -> tuple[Coord,Coord,int]:
    see(y,x,seen)
    ends = [find_end(ny,nx,seen) for ny,nx in neighs(y,x) if board[ny][nx] == "."]
    while len(ends)<2: ends.append(((y,x),0))

    (a,l1),(b,l2) = ends
    return a,b,l1+l2+1

seen = set()
secs:list[Section] = []
end_to_sec:dict[Coord,Section] = {}
i = 0
nodes = {}
for y,row in enumerate(board):
    for x,c in enumerate(row):
        if c == "." and (y,x) not in seen:
            s = Section.from_search(i,y,x,seen)
            if s.length == 1:
                nodes[s.id] = []
            i += 1
            end_to_sec[s.start] = s
            end_to_sec[s.end] = s
            secs.append(s)
            # print(s)

END_ID = -2
for _id, lst in nodes.items():
    sec:Section = secs[_id]
    for start in sec.e_exits:
        arc = end_to_sec[start]
        outs = arc.exits_from(start)
        assert len(outs)<=1
        if len(outs) == 1:
            lst.append((arc.length+3, end_to_sec[outs[0]].id))
        elif arc.start[0] != 0: # The true starting node is the other case but we dont want it
            last = _id
            lst.append((arc.length+2,END_ID))

nodes[0] = [(secs[0].length,end_to_sec[conn].id) 
            for conn in secs[0].e_exits]

d_last = next(
    d for d,_id in nodes[last] # type: ignore
    if _id == END_ID
)

rev = {
    END_ID: 0
}
i = 1
for k in nodes:
    rev[k] = i
    i *= 2
last = rev[last] # type: ignore

def wrap():
    njit_nodes = Dict.empty(types.int64,types.int64[:])
    # njit_nodes = {}
    njit_lengths = Dict.empty(types.int64,types.int64[:])
    # njit_lengths = {}
    for k,v in nodes.items():
        njit_nodes[rev[k]] = np.asarray([rev[b] for (_,b) in v], dtype='int64')
        njit_lengths[rev[k]] = np.asarray([a for (a,_) in v], dtype='int64')

    # print(njit_nodes)
    # print(njit_lengths)

# def _dfs(node,seen):
#     # if node == 0: return 0
#     return node and max(
#         (l + _dfs(target,seen | node)
#         for l,target in nodes[node]
#         if not target & seen),
#         default=NINF
#     )

    @njit
    def dfs(node,seen,njit_nodes,njit_lengths):
        if node == last: return d_last
        best = NINF
        for i,t in enumerate(njit_nodes[node]):
            if not t & seen:
                best = max(best,
                            njit_lengths[node][i] + 
                            dfs(t, seen|node, njit_nodes, njit_lengths)
                        )
        return best
    return dfs(rev[0],0,njit_nodes,njit_lengths)

l = wrap()

print(l)
print(time()-_t)