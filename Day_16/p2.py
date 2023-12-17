from pathlib import Path
from collections import deque

from tqdm import tqdm

HOME = Path(__file__).parent

def shift(i,j,d):
    if d == 0: return (i-1,j)
    if d == 1: return (i,j+1)
    if d == 2: return (i+1,j)
    if d == 3: return (i,j-1)
    raise ValueError(d)

def map_dir(todo,i,j,d,outs):
    for _d,o in enumerate(outs):
        if d == _d:
            if o>9:
                a,o = divmod(o,10)
                todo.append((*shift(i,j,a),a))
            todo.append((*shift(i,j,o),o))
            return
    raise ValueError(d)

dct = {
    ".":(0,1,2,3),
    "/":(1,0,3,2),
    "\\":(3,2,1,0),
    "-":(31,1,31,3),
    "|":(0,20,2,20)
}

def light(i,j,d):
    seen = set() # (i,j)
    seend = set() # (i,j,d)
    todo:deque[tuple[int,int,int]] = deque([(i,j,d)])
    while todo:
        i,j,d = todo.popleft()
        if i<0 or j<0 or i>=len(board) or j>=len(board[0]): continue
        if (i,j,d) in seend: continue
        seen.add((i,j))
        seend.add((i,j,d))
        map_dir(todo,i,j,d,dct[board[i][j]])
    return len(seen)


with open(HOME/"input.txt") as f:
    board = [list(line.strip()) for line in f]

    starts = []
    for i in range(len(board)):
        starts.extend(((i, 0, 1), (i, len(board[0])-1, 3)))
    for j in range(len(board[0])):
        starts.extend(((0, j, 2), (len(board)-1, j, 0)))
    print(
        max(
            map(
                lambda x: light(*x),
                tqdm(starts)
            )
        )
    )