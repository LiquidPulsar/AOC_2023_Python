from collections import defaultdict
from heapq import heappush, heappop, heapify
from pathlib import Path
from colorama import Fore, Back, Style

HOME = Path(__file__).parent

colors = "^>v<"

def shift(i,j,d):
    if d == 0: return (i-1,j)
    if d == 1: return (i,j+1)
    if d == 2: return (i+1,j)
    if d == 3: return (i,j-1)
    raise ValueError(d)

def neighbors(y,x,d,s):
    if s < 3: yield (*shift(y,x,d),d,s+1)
    n = (d+1) % 4
    yield (*shift(y,x,n),n,1)
    n = (d-1) % 4
    yield (*shift(y,x,n),n,1)

with open(HOME/"input.txt") as f:
    board = [list(map(int,line.strip())) for line in f]

    todo:list[tuple[int,int,int,int,int]] = [(0,0,1,0,0),(0,0,2,0,0)] # y,x,dir,steps,cost
    heapify(todo)

    costs = defaultdict(lambda: float("inf"))
    prev = {}
    costs[(0,0,1,0)] = 0

    while todo:
        y,x,d,s,c = heappop(todo)
        if costs[(y,x,d,s)] < s: continue

        for n in neighbors(y,x,d,s):
            ny,nx,nd,ns = n
            if ny<0 or nx<0 or ny>=len(board) or nx>=len(board[0]): continue
            if board[ny][nx] == 0: continue
            if costs[(ny,nx,nd,ns)] <= c+board[ny][nx]: continue
            prev[(ny,nx,nd,ns)] = (y,x,d,s)
            costs[(ny,nx,nd,ns)] = c+board[ny][nx]
            heappush(todo,(ny,nx,nd,ns,c+board[ny][nx]))
    print(*(costs[(len(board)-1,len(board[0])-1,a,b)] for a in range(4) for b in range(3)))
    best = min(((len(board)-1,len(board[0])-1,a,b) for a in range(4) for b in range(3)), key=lambda x: costs[x])
    print(costs[best])
    while best in prev:
        board[best[0]][best[1]] = Fore.GREEN + colors[best[2]] + Style.RESET_ALL
        best = prev[best]
    for l in board: print(*l,sep="")