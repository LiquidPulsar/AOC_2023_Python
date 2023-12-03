from pathlib import Path
HOME = Path(__file__).parent

import re


def is_clear(y,x):
    return y<0 or y>=len(board) \
            or x<0 or x>=len(board[0]) \
            or board[y][x]=="."

with open(HOME / "input.txt") as f:
    board = [l.strip() for l in f]
    tot = 0
    for y,l in enumerate(board):
        for match in re.finditer(r"\d+",l):
            # print(match)
            n = int(match.group())
            tot += n
            if not is_clear(y,match.start()-1):
                # print("clear to the left")
                continue
            if not is_clear(y,match.end()):
                # print("clear to the right")
                continue
            for x in range(match.start()-1,match.end()+1):
                if not is_clear(y-1,x) or not is_clear(y+1,x):
                    # print("blocked at",x)
                    break
            else:
                # print("found",match.group())
                tot -= n
    print(tot)