from collections import deque
from itertools import count
from pathlib import Path
from typing import Literal
from colorama import Fore, Back, Style

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

def floodfill(y:int,x:int,seen:set[tuple[int,int]]) -> int:
    q = deque([(y,x)])
    good = True
    n = 0
    while q:
        y,x = q.popleft()
        if (y,x) in seen: continue
        assert (y,x) not in loop
        seen.add((y,x))
        n += 1
        for dy,dx in deltas:
            ny,nx = y+dy,x+dx
            # Can get to outside so no.
            # Still mark the whole area as seen though.
            if 0<=ny<len(board) and 0<=nx<len(board[0]):
                if board[ny][nx] == ".":
                    assert (ny,nx) not in loop
                    q.append((ny,nx))
            else:
                good = False
    print(y,x,n,good)
    return n * good

with open(HOME/"input.txt") as f:
    start = None
    board = [[*line.rstrip()] for line in f]
    for y,line in enumerate(board):
        for X,c in enumerate(line):
            if c in tiles:
                for d in DIRS: dct[(y,X,d)] = tiles[c][d]
            elif c == "S":
                start = (y,X)
            elif c == ".":
                for d in DIRS: dct[(y,X,d)] = None

    assert start is not None
    # try each dir tile
    for letter,tile in tiles.items():
        board[start[0]][start[1]] = letter

        for d in DIRS: dct[(*start,d)] = tile[d]

        for d in DIRS:
            if dct[(*start,d)] is not None:
                break
        else: assert False

        y,X = start
        loop = set()
        for step in count(1):
            loop.add((y,X))
            d = dct.get((y,X,d))
            if d is None:
                break
            y += deltas[d][0]
            X += deltas[d][1]
            if (y,X) == start: break
        if d is None:
            print("No path for",letter)
        elif dct[(y,X,d)] is not None:
            print("Path for",letter,step,step//2) # type: ignore

            area = 0
            for Y,line in enumerate(board):
                for X,c in enumerate(line):
                    if (Y,X) not in loop:
                        left = None
                        crosses = 0
                        # print("Searching",Y,x,"...")
                        for y in range(Y):
                            # print(y,x,board[y][x],left)
                            if (y,X) not in loop: continue

                            if board[y][X] == "7":
                                left = True
                            elif board[y][X] == "F":
                                left = False
                            elif board[y][X] == "L":
                                if left: crosses += 1
                                left = None
                            elif board[y][X] == "J":
                                if left == False: crosses += 1
                                left = None
                            elif board[y][X] == "-":
                                assert left is None, (Y,X,y,left)
                                crosses += 1
                            else:
                                assert board[y][X] == "|", (Y,X,y,board[y][X])

                        # crosses = sum((y,x) in loop and board[y][x] not in "|7F" for y in range(y))
                        if crosses % 2 == 1:
                            area += 1
                            board[Y][X] = f"{Fore.GREEN}O{Style.RESET_ALL}"
                        else:
                            board[Y][X] = f"{Fore.RED}O{Style.RESET_ALL}"
            print(area)
            for y,X in loop:
                assert board[y][X] != "."
                board[y][X] = f"{Fore.BLUE}{board[y][X]}{Style.RESET_ALL}"
            for line in board: print("".join(line))