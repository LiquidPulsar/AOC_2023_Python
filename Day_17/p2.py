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

# Could do a priority queue again, and make neighbours do 4-10 steps
with open(HOME/"input.txt") as f:
    board = [list(map(int,line.strip())) for line in f]

    # todo:list[tuple[int,int,int,int,int]] = [(0,0,0,1,0),(0,0,0,2,0)] # cost,y,x,dir,steps
    # heapify(todo)

    costs = defaultdict(lambda: float("inf"))
    prev = {}
    costs[(0,0,1,0)] = 0

    todo = [[] for _ in range(10)]
    todo[0].extend([(0,0,0,1,0),(0,0,0,2,0)])

    while True:
        for c,y,x,d,s in todo[0]:
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
                todo[board[ny][nx]].append((c+board[ny][nx],ny,nx,nd,ns))
        else:
            del todo[0]
            todo.append([])
            if any(todo): continue
        break
    
    curr = best # type: ignore
    while curr in prev:
        board[curr[0]][curr[1]] = Fore.GREEN + colors[curr[2]] + Style.RESET_ALL
        # board[curr[0]][curr[1]] = f"{Fore.GREEN}{board[curr[0]][curr[1]]}{Style.RESET_ALL}"
        curr = prev[curr]

    for l in board: print(*l,sep="")
    print(c) # type: ignore