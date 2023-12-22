from collections import deque
from pathlib import Path

HOME = Path(__file__).parent

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
    print(x, y)

    todo:deque[tuple[int,int,int]] = deque([(x, y, 0)])
    visited = set()
    visited_oe = [set(),set()]
    MAX_STEPS = 64
    while todo:
        x, y, steps = todo.popleft()
        if steps > MAX_STEPS: break

        if (x, y) in visited:
            continue
        visited_oe[steps%2].add((x, y))
        visited.add((x, y))

        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            if y+dy < 0 or y+dy >= len(board) or x+dx < 0 or x+dx >= len(board[0]):
                continue
            # if board[(y + dy)%len(board)][(x + dx)%len(board[0])] != "#":
            if board[y + dy][x + dx] != "#":
                todo.append((x + dx, y + dy, steps + 1))
    # for y, row in enumerate(board):
    #     for x, col in enumerate(row):
    #         if (x, y) in visited_oe[MAX_STEPS%2]:
    #             print("O", end="")
    #         else:
    #             print(col, end="")
    #     print()
    print(len(visited_oe[MAX_STEPS%2]))