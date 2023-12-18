from collections import defaultdict
from heapq import heappush, heappop, heapify
from pathlib import Path
from colorama import Fore, Style

HOME = Path(__file__).parent

colors = "^>v<"

def shift(i,j,d):
    if d == 0: return (i-1,j)
    if d == 1: return (i,j+1)
    if d == 2: return (i+1,j)
    if d == 3: return (i,j-1)
    raise ValueError(d)

def neighbors(y,x,d,s):
    if s < 10: yield (*shift(y,x,d),d,s+1)
    if s < 4: return
    n = (d+1) % 4
    yield (*shift(y,x,n),n,1)
    n = (d-1) % 4
    yield (*shift(y,x,n),n,1)

# Improvement: replace priority queue with a list of lists
# we know the costs are always 1-9, so we can just have a list of 10 lists
with open(HOME/"input.txt") as f:
    board = [list(map(int,line.strip())) for line in f]

    todo:list[tuple[int,int,int,int,int]] = [(0,0,0,1,0),(0,0,0,2,0)] # cost,y,x,dir,steps
    heapify(todo)

    costs = defaultdict(lambda: float("inf"))
    prev = {}
    costs[(0,0,1,0)] = 0

    while todo:
        c,y,x,d,s = heappop(todo)

        if x==len(board[0])-1 and y==len(board)-1 and s>=4:
            best = (y,x,d,s)
            break

        if costs[(y,x,d,s)] < s: continue

        for n in neighbors(y,x,d,s):
            ny,nx,nd,ns = n
            if ny<0 or nx<0 or ny>=len(board) or nx>=len(board[0]): continue
            if costs[(ny,nx,nd,ns)] <= c+board[ny][nx]: continue
            prev[(ny,nx,nd,ns)] = (y,x,d,s)
            costs[(ny,nx,nd,ns)] = c+board[ny][nx]
            heappush(todo,(c+board[ny][nx],ny,nx,nd,ns))
    
    curr = best
    while curr in prev:
        board[curr[0]][curr[1]] = Fore.GREEN + colors[curr[2]] + Style.RESET_ALL
        # board[curr[0]][curr[1]] = f"{Fore.GREEN}{board[curr[0]][curr[1]]}{Style.RESET_ALL}"
        curr = prev[curr]

    for l in board: print(*l,sep="")
    print(c)