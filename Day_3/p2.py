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
    nums = {} # (y,x) -> num,start,end
    for y,l in enumerate(board):
        for match in re.finditer(r"\d+",l):
            # print(match)
            n = int(match.group())
            for x in range(match.start(),match.end()):
                nums[y,x] = (n,match.start(),match.end())

    # print(nums)

    for y,l in enumerate(board):
        for x,c in enumerate(l):
            if c == '*':
                adj = 0
                # store positions of already-accounted-for number cells so we don't loop into em
                seen = set()
                adj_tot = 1

                for dy in range(-1,2): # sourcery skip
                    for dx in range(-1,2):
                        if (dy,dx) == (0,0): continue
                        if (y+dy,x+dx) in nums and (y+dy,x+dx) not in seen:
                            num,start,end = nums[y+dy,x+dx]
                            for i in range(start,end): seen.add((y+dy,i))
                            
                            adj += 1
                            adj_tot *= num
                if adj == 2:
                    tot += adj_tot
    print(tot)