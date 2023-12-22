from collections import deque
from pathlib import Path

HOME = Path(__file__).parent

"""
26501365 is a suspicious number, could have just been 1000000000 or something

The board is 131x131
The number of steps needed 26501365, is 131 * 202300 + 65
The starting coordinate is 65,65: right in the middle of a board
After 65 steps we've just reached the edge of the board at the middle 
of each side (approx expanding diamond, is sensible)

So there are a finite nmber of types of state each sub-board can be in
"""

with open(HOME/"input.txt") as f:
    board = [list(line.strip()) for line in f]
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == "S":
                break
        else:
            continue
        break
    else:
        raise ValueError("No starting point found")
    start = (x, y)

    step_cnts = []
    for max_steps in range(65,131*3+65,131):
        todo:deque[tuple[int,int,int]] = deque([(*start, 0)])
        visited = set()
        visited_oe = [set(),set()]
        while todo:
            x, y, steps = todo.popleft()
            if steps > max_steps: break

            if (x, y) in visited:
                continue
            visited_oe[steps%2].add((x, y))
            visited.add((x, y))

            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if board[(y + dy)%len(board)][(x + dx)%len(board[0])] != "#":
                    todo.append((x + dx, y + dy, steps + 1))
        step_cnts.append(len(visited_oe[max_steps%2]))
    a,b,c = step_cnts

    def term(n): return (n**2-n) * ((c+a)//2-b) + n*(b-a) + a
    
    MAX_STEPS = 26501365
    print(MAX_STEPS,term(MAX_STEPS//131))